from fastapi import APIRouter, Depends, Query

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.sync.service import GoogleSyncService

router = APIRouter(prefix="/api/sync", tags=["sync"])


@router.post("/export-month")
async def export_month(
    year: int = Query(...),
    month: int = Query(...),
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    service = GoogleSyncService(db)
    result = service.export_month(user, year, month)
    return {
        "users_synced": result.users_synced,
        "events_synced": result.events_synced,
        "errors": result.errors,
    }


@router.get("/status")
async def sync_status(user=Depends(get_current_user), db=Depends(get_db)):
    household_size = db.count("users", {"calendar_id": f"eq.{user.calendar_id}"}) if user.calendar_id else 0
    return {
        "calendar_id": user.calendar_id,
        "household_users": household_size,
        "status": "ready",
    }
