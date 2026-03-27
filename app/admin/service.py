from __future__ import annotations

from typing import Any

from app.admin.repository import AdminRepository
from app.billing.repository import BillingRepository


ALLOWED_PLANS = {"free", "pro", "family_plus"}


class AdminService:
    def __init__(self, db):
        self.admin_repo = AdminRepository(db)
        self.billing_repo = BillingRepository(db)

    def list_users(self, offset: int = 0, limit: int = 50, search: str | None = None):
        return self.admin_repo.list_users(offset, limit, search)

    def count_users(self, search: str | None = None) -> int:
        return self.admin_repo.count_users(search)

    def get_user_detail(self, user_id: str) -> dict[str, Any] | None:
        return self.admin_repo.get_user_with_subscription(user_id)

    def change_user_plan(self, user_id: str, plan: str):
        if plan not in ALLOWED_PLANS:
            raise ValueError(f"Invalid plan: {plan}. Allowed: {', '.join(sorted(ALLOWED_PLANS))}")
        return self.billing_repo.upsert_subscription(user_id=user_id, plan=plan)

    def toggle_admin(self, user_id: str, is_admin: bool):
        return self.admin_repo.update_user_admin(user_id, is_admin)

    def get_stats(self) -> dict[str, Any]:
        return {
            "user_count": self.admin_repo.count_users(),
            "plan_distribution": self.admin_repo.get_plan_distribution(),
            "recent_signups": self.admin_repo.get_recent_signups(),
        }

    # ── Household management ──────────────────────────

    def list_households(self) -> list[dict[str, Any]]:
        return self.admin_repo.list_households()

    def get_household_detail(self, calendar_id: str) -> dict[str, Any] | None:
        return self.admin_repo.get_household_detail(calendar_id)

    def transfer_member(self, user_id: str, target_calendar_id: str) -> None:
        cal_rows = self.admin_repo.db.select(
            "calendars", {"id": f"eq.{target_calendar_id}", "limit": "1"},
        )
        if not cal_rows:
            raise ValueError("Target household not found")
        user_rows = self.admin_repo.db.select(
            "users", {"id": f"eq.{user_id}", "limit": "1"},
        )
        if not user_rows:
            raise ValueError("User not found")
        self.admin_repo.transfer_user_to_household(user_id, target_calendar_id)

    def merge_households(
        self, source_calendar_id: str, target_calendar_id: str,
    ) -> int:
        if source_calendar_id == target_calendar_id:
            raise ValueError("Source and target households must be different")
        src = self.admin_repo.db.select(
            "calendars", {"id": f"eq.{source_calendar_id}", "limit": "1"},
        )
        if not src:
            raise ValueError("Source household not found")
        tgt = self.admin_repo.db.select(
            "calendars", {"id": f"eq.{target_calendar_id}", "limit": "1"},
        )
        if not tgt:
            raise ValueError("Target household not found")
        return self.admin_repo.merge_households(
            source_calendar_id, target_calendar_id,
        )
