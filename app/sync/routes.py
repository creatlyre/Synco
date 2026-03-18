from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.sync.service import GoogleSyncService

router = APIRouter(prefix="/api/sync", tags=["sync"])


@router.post("/export-month")
async def export_month(
    year: int = Query(...),
    month: int = Query(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GoogleSyncService(db)
    result = service.export_month(user, year, month)
    return {
        "users_synced": result.users_synced,
        "events_synced": result.events_synced,
        "errors": result.errors,
    }


@router.get("/status")
async def sync_status(user=Depends(get_current_user), db: Session = Depends(get_db)):
    household_size = db.query(type(user)).filter(type(user).calendar_id == user.calendar_id).count()
    return {
        "calendar_id": user.calendar_id,
        "household_users": household_size,
        "status": "ready",
    }
