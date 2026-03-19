from datetime import datetime, timedelta

from app.events.ocr import OCRParseResult


def _payload(title: str, start: datetime, end: datetime) -> dict:
    return {
        "title": title,
        "description": "desc",
        "start_at": start.isoformat(),
        "end_at": end.isoformat(),
        "timezone": "UTC",
    }


def test_create_event(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    response = authenticated_client.post(
        "/api/events",
        json=_payload("Doctor", now + timedelta(hours=1), now + timedelta(hours=2)),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["title"] == "Doctor"


def test_update_event(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    create_response = authenticated_client.post(
        "/api/events",
        json=_payload("Initial", now + timedelta(hours=1), now + timedelta(hours=2)),
    )
    event_id = create_response.json()["id"]

    update_response = authenticated_client.put(
        f"/api/events/{event_id}",
        json={"title": "Updated Title"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"


def test_delete_event_hides_from_month(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    create_response = authenticated_client.post(
        "/api/events",
        json=_payload("Temporary", now + timedelta(hours=1), now + timedelta(hours=2)),
    )
    event_id = create_response.json()["id"]

    delete_response = authenticated_client.delete(f"/api/events/{event_id}")
    assert delete_response.status_code == 200

    month_response = authenticated_client.get(f"/api/events/month?year={now.year}&month={now.month}")
    assert month_response.status_code == 200
    ids = [item["id"] for item in month_response.json()]
    assert event_id not in ids


def test_parse_event_natural_language(authenticated_client):
    """Test parsing natural language event text."""
    response = authenticated_client.post(
        "/api/events/parse",
        json={
            "text": "dentist tomorrow 2pm",
            "context_date": "2026-03-19",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "dentist" in data["title"].lower()
    assert data["start_at"] is not None
    assert data["timezone"] is not None
    assert isinstance(data["confidence_date"], float)
    assert isinstance(data["confidence_title"], float)
    assert isinstance(data["errors"], list)


def test_parse_event_with_errors(authenticated_client):
    """Test parsing that results in errors."""
    response = authenticated_client.post(
        "/api/events/parse",
        json={
            "text": "meeting at 2pm",  # No date, only time
            "context_date": "2026-03-19",
        },
    )

    assert response.status_code == 200
    data = response.json()
    # Should either have errors or low confidence
    assert isinstance(data["errors"], list)


def test_parse_event_uses_calendar_timezone(authenticated_client, test_db, test_user_a):
    """Regression: parse endpoint should propagate user calendar timezone, not hardcoded UTC."""
    test_db.update(
        "calendars",
        {"id": f"eq.{test_user_a.calendar_id}"},
        {"timezone": "America/New_York"},
    )

    response = authenticated_client.post(
        "/api/events/parse",
        json={
            "text": "dentist tomorrow 2pm",
            "context_date": "2026-03-19",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "America/New_York"


def test_ocr_parse_event_success(authenticated_client, monkeypatch):
    now = datetime(2026, 3, 20, 14, 0, 0)

    def fake_parse_image(self, image_bytes, timezone, context_date):
        assert image_bytes == b"fake-image-bytes"
        return OCRParseResult(
            title="School concert",
            start_at=now,
            end_at=now + timedelta(hours=1),
            timezone=timezone,
            confidence_title=0.82,
            confidence_date=0.79,
            confidence_raw=0.88,
            raw_text="School concert Friday 2pm",
            errors=[],
        )

    monkeypatch.setattr("app.events.routes.OCRService.parse_image", fake_parse_image)

    response = authenticated_client.post(
        "/api/events/ocr-parse",
        data={"context_date": "2026-03-19"},
        files={"image": ("flyer.png", b"fake-image-bytes", "image/png")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "School concert"
    assert data["raw_text"] == "School concert Friday 2pm"
    assert data["confidence_raw"] == 0.88
    assert data["errors"] == []


def test_ocr_parse_event_empty_upload(authenticated_client):
    response = authenticated_client.post(
        "/api/events/ocr-parse",
        data={"context_date": "2026-03-19"},
        files={"image": ("empty.png", b"", "image/png")},
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()
