from app.budget.repository import BudgetSettingsRepository
from app.budget.schemas import BudgetSettingsUpdate
from app.database.models import BudgetSettings


class BudgetSettingsService:
    def __init__(self, repository: BudgetSettingsRepository):
        self.repository = repository

    def get_settings(self, calendar_id: str, year: int | None = None) -> BudgetSettings | None:
        return self.repository.get_by_calendar(calendar_id, year=year)

    def save_settings(self, calendar_id: str, payload: BudgetSettingsUpdate) -> BudgetSettings:
        existing = self.repository.get_by_calendar(calendar_id, year=payload.year)
        if existing:
            return self.repository.update(existing, payload)
        return self.repository.create(calendar_id, payload)
