from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any

from app.database.models import Calendar, User
from app.database.supabase_store import SupabaseStore
from app.users.repository import _to_calendar, _to_user, _parse_dt


class AdminRepository:
    def __init__(self, db: SupabaseStore):
        self.db = db

    def list_users(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> list[User]:
        params: dict[str, str] = {"order": "created_at.desc"}
        rows = self.db.select("users", params)
        if search:
            term = search.lower()
            rows = [
                r
                for r in rows
                if term in (r.get("email") or "").lower()
                or term in (r.get("name") or "").lower()
            ]
        total = len(rows)
        rows = rows[offset : offset + limit]
        return [_to_user(r) for r in rows]

    def count_users(self, search: str | None = None) -> int:
        if search:
            return len(self.list_users(0, 10000, search))
        return self.db.count("users", {})

    def get_user_with_subscription(self, user_id: str) -> dict[str, Any] | None:
        rows = self.db.select("users", {"id": f"eq.{user_id}", "limit": "1"})
        if not rows:
            return None
        user = _to_user(rows[0])
        sub_rows = self.db.select(
            "subscriptions", {"user_id": f"eq.{user_id}", "limit": "1"}
        )
        plan = "free"
        subscription = None
        if sub_rows:
            subscription = sub_rows[0]
            plan = subscription.get("plan", "free")
        return {"user": user, "plan": plan, "subscription": subscription}

    def update_user_admin(self, user_id: str, is_admin: bool) -> dict[str, Any] | None:
        return self.db.update(
            "users",
            {"id": f"eq.{user_id}"},
            {
                "is_admin": is_admin,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    def get_plan_distribution(self) -> dict[str, int]:
        rows = self.db.select("subscriptions", {})
        distribution: dict[str, int] = {}
        for row in rows:
            plan = row.get("plan", "free")
            distribution[plan] = distribution.get(plan, 0) + 1
        return distribution

    def get_recent_signups(self, days: int = 30) -> int:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        rows = self.db.select("users", {"created_at": f"gte.{cutoff}"})
        return len(rows)

    # ── Household management ──────────────────────────────────

    def list_households(self) -> list[dict[str, Any]]:
        cal_rows = self.db.select("calendars", {"order": "created_at.desc"})
        user_rows = self.db.select("users", {})

        users_by_cal: dict[str, list[User]] = {}
        for r in user_rows:
            cid = r.get("calendar_id")
            if cid:
                users_by_cal.setdefault(cid, []).append(_to_user(r))

        result: list[dict[str, Any]] = []
        for cr in cal_rows:
            cal = _to_calendar(cr)
            members = users_by_cal.get(cal.id, [])
            owner = next((m for m in members if m.id == cal.owner_user_id), None)
            result.append({"calendar": cal, "members": members, "owner": owner})
        return result

    def get_household_detail(self, calendar_id: str) -> dict[str, Any] | None:
        rows = self.db.select("calendars", {"id": f"eq.{calendar_id}", "limit": "1"})
        if not rows:
            return None
        cal = _to_calendar(rows[0])
        member_rows = self.db.select("users", {"calendar_id": f"eq.{calendar_id}"})
        members = [_to_user(r) for r in member_rows]
        owner = next((m for m in members if m.id == cal.owner_user_id), None)
        return {"calendar": cal, "members": members, "owner": owner}

    def transfer_user_to_household(
        self, user_id: str, target_calendar_id: str,
    ) -> None:
        self.db.update(
            "users",
            {"id": f"eq.{user_id}"},
            {
                "calendar_id": target_calendar_id,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    def merge_households(
        self, source_calendar_id: str, target_calendar_id: str,
    ) -> int:
        rows = self.db.select(
            "users", {"calendar_id": f"eq.{source_calendar_id}"},
        )
        for r in rows:
            self.db.update(
                "users",
                {"id": f"eq.{r['id']}"},
                {
                    "calendar_id": target_calendar_id,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                },
            )
        return len(rows)
