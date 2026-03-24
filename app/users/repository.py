from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import uuid

from app.database.models import Calendar, CalendarInvitation, User
from app.database.supabase_store import SupabaseStore


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is not None:
            return parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    except ValueError:
        return None


def _to_user(row: dict[str, Any]) -> User:
    return User(
        id=row.get("id", ""),
        email=row.get("email", ""),
        name=row.get("name") or "",
        google_id=row.get("google_id"),
        google_access_token=row.get("google_access_token"),
        google_refresh_token=row.get("google_refresh_token"),
        google_token_expiry=_parse_dt(row.get("google_token_expiry")),
        calendar_id=row.get("calendar_id"),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
        last_login=_parse_dt(row.get("last_login")),
        is_admin=bool(row.get("is_admin", False)),
    )


def _to_calendar(row: dict[str, Any]) -> Calendar:
    return Calendar(
        id=row.get("id", ""),
        name=row.get("name") or "",
        timezone=row.get("timezone") or "UTC",
        owner_user_id=row.get("owner_user_id"),
        google_calendar_id=row.get("google_calendar_id"),
        last_sync_at=_parse_dt(row.get("last_sync_at")),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
    )


def _to_invitation(row: dict[str, Any]) -> CalendarInvitation:
    return CalendarInvitation(
        id=row.get("id", ""),
        calendar_id=row.get("calendar_id", ""),
        invited_email=row.get("invited_email", ""),
        inviter_user_id=row.get("inviter_user_id"),
        status=row.get("status") or "pending",
        created_at=_parse_dt(row.get("created_at")),
        expires_at=_parse_dt(row.get("expires_at")),
    )


class UserRepository:
    def __init__(self, db: SupabaseStore):
        self.db = db

    def get_user_by_id(self, user_id: str, auth_token: str | None = None) -> User | None:
        rows = self.db.select("users", {"id": f"eq.{user_id}", "limit": "1"}, auth_token=auth_token)
        return _to_user(rows[0]) if rows else None

    def get_user_by_email(self, email: str, auth_token: str | None = None) -> User | None:
        rows = self.db.select("users", {"email": f"eq.{email.lower()}", "limit": "1"}, auth_token=auth_token)
        return _to_user(rows[0]) if rows else None

    def get_user_by_external_id(self, external_id: str, auth_token: str | None = None) -> User | None:
        rows = self.db.select("users", {"google_id": f"eq.{external_id}", "limit": "1"}, auth_token=auth_token)
        return _to_user(rows[0]) if rows else None

    def create_user(self, payload: dict[str, Any], auth_token: str | None = None) -> User:
        row = self.db.insert("users", payload, auth_token=auth_token)
        return _to_user(row)

    def update_user(self, user_id: str, payload: dict[str, Any], auth_token: str | None = None) -> User | None:
        row = self.db.update("users", {"id": f"eq.{user_id}"}, payload, auth_token=auth_token)
        return _to_user(row) if row else None

    def get_calendar_by_id(self, calendar_id: str, auth_token: str | None = None) -> Calendar | None:
        rows = self.db.select("calendars", {"id": f"eq.{calendar_id}", "limit": "1"}, auth_token=auth_token)
        return _to_calendar(rows[0]) if rows else None

    def create_calendar(self, payload: dict[str, Any], auth_token: str | None = None) -> Calendar:
        row = self.db.insert("calendars", payload, auth_token=auth_token)
        return _to_calendar(row)

    def create_invitation(
        self,
        calendar_id: str,
        invited_email: str,
        inviter_user_id: str,
        auth_token: str | None = None,
    ) -> CalendarInvitation:
        row = self.db.insert(
            "calendar_invitations",
            {
                "id": str(uuid.uuid4()),
                "calendar_id": calendar_id,
                "invited_email": invited_email.lower(),
                "inviter_user_id": inviter_user_id,
                "status": "pending",
            },
            auth_token=auth_token,
        )
        return _to_invitation(row)

    def get_pending_invitations(self, email: str) -> list[CalendarInvitation]:
        rows = self.db.select(
            "calendar_invitations",
            {
                "invited_email": f"eq.{email.lower()}",
                "status": "eq.pending",
                "order": "created_at.asc",
            },
        )
        return [_to_invitation(item) for item in rows]

    def accept_invitation(self, invitation_id: str, user_id: str) -> User | None:
        invitation_rows = self.db.select("calendar_invitations", {"id": f"eq.{invitation_id}", "limit": "1"})
        user_rows = self.db.select("users", {"id": f"eq.{user_id}", "limit": "1"})
        if not invitation_rows or not user_rows:
            return None

        invitation = invitation_rows[0]
        user = user_rows[0]

        self.db.update("users", {"id": f"eq.{user_id}"}, {"calendar_id": invitation.get("calendar_id")})
        self.db.update("calendar_invitations", {"id": f"eq.{invitation_id}"}, {"status": "accepted"})

        updated_rows = self.db.select("users", {"id": f"eq.{user_id}", "limit": "1"})
        return _to_user(updated_rows[0]) if updated_rows else _to_user(user)

    def get_users_by_calendar_id(self, calendar_id: str) -> list[User]:
        rows = self.db.select("users", {"calendar_id": f"eq.{calendar_id}"})
        return [_to_user(item) for item in rows]

    def get_household_members(self, user_id: str) -> list[User]:
        user = self.get_user_by_id(user_id)
        if not user or not user.calendar_id:
            return []

        return self.get_users_by_calendar_id(user.calendar_id)

    def get_household_calendar(self, user_id: str) -> Calendar | None:
        user = self.get_user_by_id(user_id)
        if not user or not user.calendar_id:
            return None

        return self.get_calendar_by_id(user.calendar_id)
