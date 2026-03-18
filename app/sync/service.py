from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from sqlalchemy.orm import Session

from app.auth.oauth import refresh_access_token
from app.auth.utils import decrypt_token, encrypt_token
from app.database.models import Event, User
from app.events.repository import EventRepository
from app.events.service import EventService
from config import Settings


@dataclass
class SyncResult:
    users_synced: int
    events_synced: int
    errors: list[str]


class GoogleSyncService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = Settings()

    def _household_users(self, calendar_id: str) -> list[User]:
        return self.db.query(User).filter(User.calendar_id == calendar_id).all()

    def _credentials_for_user(self, user: User) -> Credentials | None:
        if not user.google_refresh_token and not user.google_access_token:
            return None

        token = decrypt_token(user.google_access_token) if user.google_access_token else None
        refresh_token = decrypt_token(user.google_refresh_token) if user.google_refresh_token else None

        creds = Credentials(
            token=token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.settings.GOOGLE_CLIENT_ID,
            client_secret=self.settings.GOOGLE_CLIENT_SECRET,
            scopes=self.settings.GOOGLE_SCOPES,
        )

        if user.google_token_expiry and user.google_token_expiry <= datetime.utcnow() and refresh_token:
            refreshed = refresh_access_token(refresh_token)
            if not refreshed:
                return None
            user.google_access_token = encrypt_token(refreshed["access_token"])
            if refreshed.get("refresh_token"):
                user.google_refresh_token = encrypt_token(refreshed["refresh_token"])
            user.google_token_expiry = refreshed.get("token_expiry")
            self.db.add(user)
            self.db.commit()

            creds = Credentials(
                token=refreshed["access_token"],
                refresh_token=decrypt_token(user.google_refresh_token) if user.google_refresh_token else None,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.settings.GOOGLE_CLIENT_ID,
                client_secret=self.settings.GOOGLE_CLIENT_SECRET,
                scopes=self.settings.GOOGLE_SCOPES,
            )

        return creds

    @staticmethod
    def _sync_calendar_name(user: User) -> str:
        suffix = user.email.split("@")[0] if user.email else user.id[:8]
        return f"CalendarPlanner Sync ({suffix})"

    def _google_service(self, creds: Credentials):
        return build("calendar", "v3", credentials=creds, cache_discovery=False)

    def _ensure_user_calendar(self, service, user: User) -> str:
        target_name = self._sync_calendar_name(user)
        calendars = service.calendarList().list().execute().get("items", [])

        for cal in calendars:
            if cal.get("summary") == target_name:
                return cal["id"]

        created = service.calendars().insert(body={"summary": target_name, "timeZone": "UTC"}).execute()
        return created["id"]

    @staticmethod
    def _event_body(event: Event) -> dict:
        return {
            "summary": event.title,
            "description": event.description or "",
            "start": {"dateTime": event.start_at.isoformat(), "timeZone": event.timezone or "UTC"},
            "end": {"dateTime": event.end_at.isoformat(), "timeZone": event.timezone or "UTC"},
            "recurrence": [f"RRULE:{event.rrule}"] if event.rrule else [],
            "extendedProperties": {"private": {"cp_event_id": event.id}},
        }

    def _find_google_event(self, service, calendar_id: str, app_event_id: str):
        items = (
            service.events()
            .list(calendarId=calendar_id, privateExtendedProperty=f"cp_event_id={app_event_id}", showDeleted=True)
            .execute()
            .get("items", [])
        )
        return items[0] if items else None

    def sync_event_for_household(self, event: Event, deleted: bool = False) -> SyncResult:
        users = self._household_users(event.calendar_id)
        synced_users = 0
        synced_events = 0
        errors: list[str] = []

        for user in users:
            try:
                creds = self._credentials_for_user(user)
                if not creds:
                    continue

                service = self._google_service(creds)
                calendar_id = self._ensure_user_calendar(service, user)
                existing = self._find_google_event(service, calendar_id, event.id)

                if deleted:
                    if existing:
                        service.events().delete(calendarId=calendar_id, eventId=existing["id"]).execute()
                        synced_events += 1
                else:
                    payload = self._event_body(event)
                    if existing:
                        service.events().update(calendarId=calendar_id, eventId=existing["id"], body=payload).execute()
                    else:
                        service.events().insert(calendarId=calendar_id, body=payload).execute()
                    synced_events += 1

                synced_users += 1
            except Exception as exc:
                errors.append(f"{user.email}: {exc}")

        if hasattr(event, "google_sync_at"):
            event.google_sync_at = datetime.utcnow()
            self.db.add(event)
            self.db.commit()
        return SyncResult(users_synced=synced_users, events_synced=synced_events, errors=errors)

    def export_month(self, user: User, year: int, month: int) -> SyncResult:
        service = EventService(EventRepository(self.db))
        events = service.list_month_expanded(user.calendar_id, year, month)

        total_users = 0
        total_events = 0
        errors: list[str] = []
        for item in events:
            if not hasattr(item, "calendar_id"):
                continue
            result = self.sync_event_for_household(item, deleted=False)
            total_users += result.users_synced
            total_events += result.events_synced
            errors.extend(result.errors)

        return SyncResult(users_synced=total_users, events_synced=total_events, errors=errors)
