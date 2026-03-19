from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.events.nlp import NLPService, ParseResult
from app.events.repository import EventRepository
from app.events.schemas import EventCreate, EventResponse, EventUpdate
from app.events.service import EventService
from app.sync.service import GoogleSyncService

router = APIRouter(prefix="/api/events", tags=["events"])


class ParseEventRequest(BaseModel):
    """Request to parse natural language event text."""

    text: str
    context_date: Optional[str] = None  # ISO date, defaults to today


class ParseEventResponse(BaseModel):
    """Response from parsing natural language event text."""

    title: str
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    timezone: str
    confidence_date: float
    confidence_title: float
    recurrence: Optional[dict] = None
    errors: list[str]
    raw_text: str


def _service(db) -> EventService:
    return EventService(EventRepository(db))


@router.post("/parse", response_model=ParseEventResponse)
async def parse_event(payload: ParseEventRequest, user=Depends(get_current_user), db=Depends(get_db)):
    """Parse natural language text into structured event data."""
    # Determine context date
    context_date = None
    if payload.context_date:
        try:
            context_date = datetime.fromisoformat(payload.context_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid context_date format, use ISO 8601") from None
    
    # For now, use UTC timezone (could be enhanced to fetch from calendar metadata)
    timezone = "UTC"
    
    # Parse the text
    nlp = NLPService()
    result = nlp.parse(payload.text, timezone, context_date)

    # Return as response model
    return ParseEventResponse(
        title=result.title,
        start_at=result.start_at,
        end_at=result.end_at,
        timezone=timezone,
        confidence_date=result.confidence_date,
        confidence_title=result.confidence_title,
        recurrence=result.recurrence,
        errors=result.errors,
        raw_text=result.raw_text,
    )


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate, user=Depends(get_current_user), db=Depends(get_db)):
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
async def update_event(event_id: str, payload: EventUpdate, user=Depends(get_current_user), db=Depends(get_db)):
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
async def delete_event(event_id: str, user=Depends(get_current_user), db=Depends(get_db)):
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
    db=Depends(get_db),
):
    service = _service(db)
    return service.list_day(user.calendar_id, year, month, day)


@router.get("/month", response_model=list[EventResponse])
async def list_month(
    year: int = Query(...),
    month: int = Query(...),
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    service = _service(db)
    return service.list_month(user.calendar_id, year, month)
