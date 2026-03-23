from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.budget.repository import BudgetSettingsRepository
from app.budget.schemas import BudgetSettingsResponse, BudgetSettingsUpdate
from app.budget.service import BudgetSettingsService
from app.database.database import get_db

router = APIRouter(prefix="/api/budget", tags=["budget"])


def _service(db) -> BudgetSettingsService:
    return BudgetSettingsService(BudgetSettingsRepository(db))


@router.get("/settings")
async def get_budget_settings(year: int, user=Depends(get_current_user), db=Depends(get_db)):
    service = _service(db)
    settings = service.get_settings(user.calendar_id, year=year)
    if not settings:
        return {"data": None}
    return {"data": BudgetSettingsResponse.model_validate(settings, from_attributes=True).model_dump()}


@router.put("/settings")
async def update_budget_settings(
    payload: BudgetSettingsUpdate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    settings = service.save_settings(user.calendar_id, payload)
    return {"data": BudgetSettingsResponse.model_validate(settings, from_attributes=True).model_dump()}
