from __future__ import annotations

from datetime import datetime, timezone

from app.database.models import BudgetSettings
from app.database.supabase_store import SupabaseStore
from app.budget.schemas import BudgetSettingsUpdate


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


def _to_budget_settings(row: dict) -> BudgetSettings:
    return BudgetSettings(
        id=row.get("id", ""),
        calendar_id=row.get("calendar_id", ""),
        rate_1=float(row.get("rate_1", 0)),
        rate_2=float(row.get("rate_2", 0)),
        rate_3=float(row.get("rate_3", 0)),
        zus_costs=float(row.get("zus_costs", 0)),
        accounting_costs=float(row.get("accounting_costs", 0)),
        initial_balance=float(row.get("initial_balance", 0)),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
    )


class BudgetSettingsRepository:
    def __init__(self, db: SupabaseStore):
        self.db = db

    def get_by_calendar(self, calendar_id: str) -> BudgetSettings | None:
        rows = self.db.select(
            "budget_settings",
            {"calendar_id": f"eq.{calendar_id}", "limit": "1"},
        )
        return _to_budget_settings(rows[0]) if rows else None

    def create(self, calendar_id: str, payload: BudgetSettingsUpdate) -> BudgetSettings:
        row = self.db.insert(
            "budget_settings",
            {
                "calendar_id": calendar_id,
                "rate_1": payload.rate_1,
                "rate_2": payload.rate_2,
                "rate_3": payload.rate_3,
                "zus_costs": payload.zus_costs,
                "accounting_costs": payload.accounting_costs,
                "initial_balance": payload.initial_balance,
            },
        )
        return _to_budget_settings(row)

    def update(self, settings: BudgetSettings, payload: BudgetSettingsUpdate) -> BudgetSettings:
        row = self.db.update(
            "budget_settings",
            {"id": f"eq.{settings.id}"},
            {
                "rate_1": payload.rate_1,
                "rate_2": payload.rate_2,
                "rate_3": payload.rate_3,
                "zus_costs": payload.zus_costs,
                "accounting_costs": payload.accounting_costs,
                "initial_balance": payload.initial_balance,
                "updated_at": datetime.utcnow().isoformat(),
            },
        )
        return _to_budget_settings(row) if row else settings
