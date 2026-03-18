from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.events.repository import EventRepository
from app.events.schemas import EventCreate, EventResponse, EventUpdate
from app.events.service import EventService
from app.sync.service import GoogleSyncService

router = APIRouter(prefix="/api/events", tags=["events"])


def _service(db: Session) -> EventService:
    return EventService(EventRepository(db))


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = _service(db)
    try:
        event = service.create_event(user.calendar_id, user.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        GoogleSyncService(db).sync_event_for_household(event, deleted=False)
    except Exception:
        pass
    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(event_id: str, payload: EventUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = _service(db)
    try:
        event = service.update_event(event_id, user.calendar_id, user.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    try:
        GoogleSyncService(db).sync_event_for_household(event, deleted=False)
    except Exception:
        pass
    return event


@router.delete("/{event_id}")
async def delete_event(event_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = _service(db)
    try:
        event = service.delete_event(event_id, user.calendar_id, user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    try:
        GoogleSyncService(db).sync_event_for_household(event, deleted=True)
    except Exception:
        pass
    return {"message": "deleted"}


@router.get("/day", response_model=list[EventResponse])
async def list_day(
    year: int = Query(...),
    month: int = Query(...),
    day: int = Query(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = _service(db)
    return service.list_day(user.calendar_id, year, month, day)


@router.get("/month", response_model=list[EventResponse])
async def list_month(
    year: int = Query(...),
    month: int = Query(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = _service(db)
    return service.list_month(user.calendar_id, year, month)
