from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.budget.expense_repository import ExpenseRepository
from app.budget.income_repository import MonthlyHoursRepository, AdditionalEarningsRepository
from app.budget.overview_service import OverviewService
from app.budget.repository import BudgetSettingsRepository
from app.database.database import get_db

router = APIRouter(prefix="/api/budget/overview", tags=["overview"])


def _service(db) -> OverviewService:
    return OverviewService(
        BudgetSettingsRepository(db),
        MonthlyHoursRepository(db),
        AdditionalEarningsRepository(db),
        ExpenseRepository(db),
    )


@router.get("/comparison")
async def get_comparison(year: int, user=Depends(get_current_user), db=Depends(get_db)):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    data = service.get_year_comparison(user.calendar_id, year)
    return {"data": data}


@router.get("")
async def get_overview(year: int, user=Depends(get_current_user), db=Depends(get_db)):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    data = service.get_year_overview(user.calendar_id, year)
    year_bounds = service.get_year_bounds(user.calendar_id)
    return {"data": data, "year_bounds": year_bounds}
