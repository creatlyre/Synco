from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

from app.events.schemas import (
    CategoryCreate,
    CategoryResponse,
    EventCreate,
    EventUpdate,
    EventResponse,
)

def test_category_create_valid():
    category = CategoryCreate(name="Work", color="#ff0000")
    assert category.name == "Work"
    assert category.color == "#ff0000"

def test_category_create_invalid_name():
    with pytest.raises(ValidationError):
        CategoryCreate(name="", color="#ff0000")

    with pytest.raises(ValidationError):
        CategoryCreate(name="a" * 51, color="#ff0000")

def test_category_create_invalid_color():
    with pytest.raises(ValidationError):
        CategoryCreate(name="Work", color="ff0000")

    with pytest.raises(ValidationError):
        CategoryCreate(name="Work", color="#ff000")

    with pytest.raises(ValidationError):
        CategoryCreate(name="Work", color="#gg0000")

def test_event_create_valid():
    start = datetime.now(timezone.utc)
    end = datetime.now(timezone.utc)
    event = EventCreate(title="Meeting", start_at=start, end_at=end)
    assert event.title == "Meeting"
    assert event.start_at == start
    assert event.end_at == end
    assert event.timezone == "UTC"
    assert event.visibility == "shared"

def test_event_create_invalid_title():
    start = datetime.now(timezone.utc)
    end = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        EventCreate(title="", start_at=start, end_at=end)

    with pytest.raises(ValidationError):
        EventCreate(title="a" * 256, start_at=start, end_at=end)

def test_event_create_reminder_minutes_list():
    start = datetime.now(timezone.utc)
    end = datetime.now(timezone.utc)

    # Valid
    event = EventCreate(title="Meeting", start_at=start, end_at=end, reminder_minutes_list=[10, 60])
    assert event.reminder_minutes_list == [10, 60]

    # Invalid negative
    with pytest.raises(ValidationError, match="reminder minutes must be non-negative"):
        EventCreate(title="Meeting", start_at=start, end_at=end, reminder_minutes_list=[-10])

    # Invalid too large
    with pytest.raises(ValidationError, match="reminder minutes cannot exceed 40320"):
        EventCreate(title="Meeting", start_at=start, end_at=end, reminder_minutes_list=[50000])

def test_event_update_valid():
    event = EventUpdate(title="New Meeting")
    assert event.title == "New Meeting"
    assert event.description is None

def test_event_update_invalid_title():
    with pytest.raises(ValidationError):
        EventUpdate(title="")

    with pytest.raises(ValidationError):
        EventUpdate(title="a" * 256)

def test_category_response_from_attributes():
    class DummyModel:
        id = "cat-123"
        calendar_id = "cal-456"
        name = "Personal"
        color = "#00ff00"
        is_preset = True
        sort_order = 1

    dummy = DummyModel()
    cat_resp = CategoryResponse.model_validate(dummy)
    assert cat_resp.id == "cat-123"
    assert cat_resp.name == "Personal"
    assert cat_resp.is_preset is True

def test_event_response_from_attributes():
    class DummyModel:
        id = "evt-123"
        calendar_id = "cal-456"
        created_by_user_id = "user-789"
        title = "Sync"
        description = "Weekly sync"
        start_at = datetime.now(timezone.utc)
        end_at = datetime.now(timezone.utc)
        timezone = "UTC"
        is_deleted = False
        rrule = None
        visibility = "shared"
        category_id = "cat-123"
        reminder_minutes = None
        reminder_minutes_list = [15, 60]

    dummy = DummyModel()
    evt_resp = EventResponse.model_validate(dummy)
    assert evt_resp.id == "evt-123"
    assert evt_resp.title == "Sync"
    assert evt_resp.reminder_minutes_list == [15, 60]
    assert evt_resp.is_deleted is False
