from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.database.models import Event
from app.database.supabase_store import SupabaseStore
from app.events.schemas import EventCreate, EventUpdate


def _to_iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


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


def _to_event(row: dict[str, Any]) -> Event:
    return Event(
        id=row.get("id", ""),
        calendar_id=row.get("calendar_id", ""),
        created_by_user_id=row.get("created_by_user_id"),
        title=row.get("title") or "",
        description=row.get("description"),
        start_at=_parse_dt(row.get("start_at")),
        end_at=_parse_dt(row.get("end_at")),
        timezone=row.get("timezone") or "UTC",
        rrule=row.get("rrule"),
        google_event_id=row.get("google_event_id"),
        google_sync_at=_parse_dt(row.get("google_sync_at")),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
        last_edited_by_user_id=row.get("last_edited_by_user_id"),
        is_deleted=bool(row.get("is_deleted", False)),
    )


class EventRepository:
    def __init__(self, db: SupabaseStore):
        self.db = db

    def create(self, calendar_id: str, user_id: str, payload: EventCreate) -> Event:
        row = self.db.insert(
            "events",
            {
                "calendar_id": calendar_id,
                "created_by_user_id": user_id,
                "last_edited_by_user_id": user_id,
                "title": payload.title,
                "description": payload.description,
                "start_at": _to_iso(payload.start_at),
                "end_at": _to_iso(payload.end_at),
                "timezone": payload.timezone,
                "rrule": payload.rrule,
                "is_deleted": False,
            },
        )
        return _to_event(row)

    def get_by_id(self, event_id: str, calendar_id: str) -> Event | None:
        rows = self.db.select(
            "events",
            {
                "id": f"eq.{event_id}",
                "calendar_id": f"eq.{calendar_id}",
                "is_deleted": "eq.false",
                "limit": "1",
            },
        )
        return _to_event(rows[0]) if rows else None

    def update(self, event: Event, user_id: str, payload: EventUpdate) -> Event:
        update_data = payload.model_dump(exclude_unset=True)
        body: dict[str, Any] = {
            "last_edited_by_user_id": user_id,
            "updated_at": datetime.utcnow().isoformat(),
        }
        for key, value in update_data.items():
            if isinstance(value, datetime):
                body[key] = value.isoformat()
            else:
                body[key] = value

        row = self.db.update(
            "events",
            {
                "id": f"eq.{event.id}",
                "calendar_id": f"eq.{event.calendar_id}",
            },
            body,
        )
        return _to_event(row) if row else event

    def soft_delete(self, event: Event, user_id: str) -> Event:
        row = self.db.update(
            "events",
            {
                "id": f"eq.{event.id}",
                "calendar_id": f"eq.{event.calendar_id}",
            },
            {
                "is_deleted": True,
                "last_edited_by_user_id": user_id,
                "updated_at": datetime.utcnow().isoformat(),
            },
        )
        return _to_event(row) if row else event

    def _all_active_for_calendar(self, calendar_id: str) -> list[Event]:
        rows = self.db.select("events", {"calendar_id": f"eq.{calendar_id}", "is_deleted": "eq.false"})
        events = [_to_event(item) for item in rows]
        return [item for item in events if item.start_at is not None]

    def list_for_day(self, calendar_id: str, year: int, month: int, day: int) -> list[Event]:
        day_start = datetime(year, month, day, 0, 0, 0)
        day_end = datetime(year, month, day, 23, 59, 59)
        events = [
            item
            for item in self._all_active_for_calendar(calendar_id)
            if item.rrule is None and item.start_at and day_start <= item.start_at <= day_end
        ]
        return sorted(events, key=lambda item: item.start_at or datetime.min)

    def list_for_month(self, calendar_id: str, year: int, month: int) -> list[Event]:
        events = [
            item
            for item in self._all_active_for_calendar(calendar_id)
            if item.rrule is None and item.start_at and item.start_at.year == year and item.start_at.month == month
        ]
        return sorted(events, key=lambda item: item.start_at or datetime.min)

    def list_recurrence_roots_until(self, calendar_id: str, range_end: datetime) -> list[Event]:
        events = [
            item
            for item in self._all_active_for_calendar(calendar_id)
            if item.rrule is not None and item.start_at and item.start_at <= range_end
        ]
        return sorted(events, key=lambda item: item.start_at or datetime.min)
