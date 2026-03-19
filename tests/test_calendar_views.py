import uuid
from datetime import datetime, timedelta

from app.database.models import Event


def test_month_view_renders_event_title_and_time(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    authenticated_client.post(
        "/api/events",
        json={
            "title": "Gym",
            "description": "Workout",
            "start_at": (now + timedelta(hours=1)).isoformat(),
            "end_at": (now + timedelta(hours=2)).isoformat(),
            "timezone": "UTC",
        },
    )

    response = authenticated_client.get(f"/calendar/month?year={now.year}&month={now.month}")
    assert response.status_code == 200
    assert "Gym" in response.text


def test_day_view_renders_event(authenticated_client):
    now = datetime.utcnow().replace(hour=12, minute=0, second=0, microsecond=0)
    authenticated_client.post(
        "/api/events",
        json={
            "title": "Lunch",
            "description": "Cafe",
            "start_at": (now + timedelta(hours=3)).isoformat(),
            "end_at": (now + timedelta(hours=4)).isoformat(),
            "timezone": "UTC",
        },
    )

    response = authenticated_client.get(f"/calendar/day?year={now.year}&month={now.month}&day={now.day}")
    assert response.status_code == 200
    assert "Lunch" in response.text


def test_month_navigation_changes_label(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)

    current_response = authenticated_client.get(f"/calendar/month?year={now.year}&month={now.month}")
    assert current_response.status_code == 200

    next_month = 1 if now.month == 12 else now.month + 1
    next_year = now.year + 1 if now.month == 12 else now.year

    next_response = authenticated_client.get(f"/calendar/month?year={next_year}&month={next_month}")
    assert next_response.status_code == 200
    assert current_response.text != next_response.text


def test_month_view_ignores_malformed_recurrence_rule(authenticated_client, test_user_a, test_db):
    now = datetime.utcnow().replace(microsecond=0)
    bad_rrule_event = Event(
        id=str(uuid.uuid4()),
        calendar_id=test_user_a.calendar_id,
        created_by_user_id=test_user_a.id,
        last_edited_by_user_id=test_user_a.id,
        title="Broken Recurrence",
        description="Legacy invalid RRULE",
        start_at=now,
        end_at=now + timedelta(hours=1),
        timezone="UTC",
        rrule="NOT_A_VALID_RRULE",
    )
    test_db.add(bad_rrule_event)
    test_db.commit()

    response = authenticated_client.get(f"/calendar/month?year={now.year}&month={now.month}")
    assert response.status_code == 200


def test_day_view_ignores_malformed_recurrence_rule(authenticated_client, test_user_a, test_db):
    now = datetime.utcnow().replace(hour=12, minute=0, second=0, microsecond=0)
    bad_rrule_event = Event(
        id=str(uuid.uuid4()),
        calendar_id=test_user_a.calendar_id,
        created_by_user_id=test_user_a.id,
        last_edited_by_user_id=test_user_a.id,
        title="Broken Recurrence",
        description="Legacy invalid RRULE",
        start_at=now,
        end_at=now + timedelta(hours=1),
        timezone="UTC",
        rrule="NOT_A_VALID_RRULE",
    )
    test_db.add(bad_rrule_event)
    test_db.commit()

    response = authenticated_client.get(f"/calendar/day?year={now.year}&month={now.month}&day={now.day}")
    assert response.status_code == 200


# ── Quick Add modal (server-rendered HTML presence) ───────────────────────────

def test_quick_add_button_present_on_calendar_page(authenticated_client):
    """Quick Add button is rendered in the Event Editor card."""
    response = authenticated_client.get("/")
    assert response.status_code == 200
    assert 'id="qa-open-btn"' in response.text


def test_quick_add_modal_markup_present(authenticated_client):
    """Modal container and key phases are present in the page HTML."""
    response = authenticated_client.get("/")
    assert response.status_code == 200
    html = response.text
    assert 'id="quick-add-modal"' in html
    assert 'id="qa-text-entry"' in html
    assert 'id="qa-text-input"' in html
    assert 'id="qa-parse-btn"' in html
    assert 'id="qa-review-phase"' in html
    assert 'id="qa-loading"' in html


def test_quick_add_review_form_fields_present(authenticated_client):
    """Review form contains all required input fields."""
    response = authenticated_client.get("/")
    assert response.status_code == 200
    html = response.text
    assert 'id="qa-parsed-title"' in html
    assert 'id="qa-parsed-start"' in html
    assert 'id="qa-parsed-end"' in html
    assert 'id="qa-parsed-repeat"' in html
    assert 'id="qa-parsed-count"' in html
    assert 'id="qa-parsed-until"' in html
    assert 'id="qa-save-btn"' in html
    assert 'id="qa-save-another-btn"' in html
    assert 'id="qa-back-btn"' in html


def test_quick_add_parse_endpoint_reachable(authenticated_client):
    """POST /api/events/parse returns a valid ParseResult for a simple phrase."""
    from datetime import date
    response = authenticated_client.post(
        "/api/events/parse",
        json={"text": "dentist tomorrow", "context_date": date.today().isoformat()},
    )
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "start_at" in data


def test_quick_add_error_area_markup_present(authenticated_client):
    """Inline error area and 'Edit text' link are present in the modal HTML."""
    response = authenticated_client.get("/")
    assert response.status_code == 200
    html = response.text
    assert 'id="qa-error-inline"' in html
    assert 'id="qa-error-summary"' in html
    assert 'id="qa-save-error"' in html


def test_quick_add_save_event_via_api(authenticated_client):
    """Saving a quick-add event via POST /api/events works end-to-end."""
    from datetime import datetime, timedelta
    now = datetime.utcnow().replace(microsecond=0)
    response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Quick add test event",
            "start_at": (now + timedelta(hours=2)).isoformat(),
            "end_at": (now + timedelta(hours=3)).isoformat(),
            "timezone": "UTC",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Quick add test event"


def test_quick_add_js_orchestration_present(authenticated_client):
    """JavaScript for quick-add orchestration is embedded in the page."""
    response = authenticated_client.get("/")
    assert response.status_code == 200
    html = response.text
    # Core JS function names from the orchestration block
    assert "qa-parse-btn" in html
    assert "/api/events/parse" in html
    assert "saveEvent" in html
    assert "resetModal" in html


def test_quick_add_escape_guard_code_present(authenticated_client):
    """Escape-key guard (no close during in-flight save) is in page JS."""
    response = authenticated_client.get("/")
    assert response.status_code == 200
    assert "_saveInFlight" in response.text


def test_quick_add_mobile_css_present(authenticated_client):
    """Mobile full-screen CSS override for modal is in the page."""
    response = authenticated_client.get("/")
    assert response.status_code == 200
    assert "max-width: 640px" in response.text
    assert "qa-modal-panel" in response.text
