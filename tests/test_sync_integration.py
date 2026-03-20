def test_event_create_triggers_sync(authenticated_client, monkeypatch):
    called = {"count": 0, "deleted": None}

    class FakeResult:
        users_synced = 1
        events_synced = 1
        errors = []

    def fake_sync(self, event, deleted=False):
        called["count"] += 1
        called["deleted"] = deleted
        return FakeResult()

    import app.sync.service

    monkeypatch.setattr(app.sync.service.GoogleSyncService, "sync_event_for_household", fake_sync)

    response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Sync Test",
            "description": None,
            "start_at": "2026-03-18T10:00:00",
            "end_at": "2026-03-18T11:00:00",
            "timezone": "UTC",
        },
    )

    assert response.status_code == 201
    assert called["count"] == 1
    assert called["deleted"] is False


def test_event_delete_triggers_delete_sync(authenticated_client, monkeypatch):
    called = {"count": 0, "deleted": None}

    class FakeResult:
        users_synced = 1
        events_synced = 1
        errors = []

    def fake_sync(self, event, deleted=False):
        called["count"] += 1
        called["deleted"] = deleted
        return FakeResult()

    import app.sync.service

    monkeypatch.setattr(app.sync.service.GoogleSyncService, "sync_event_for_household", fake_sync)

    create_response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Delete Sync",
            "description": None,
            "start_at": "2026-03-18T12:00:00",
            "end_at": "2026-03-18T13:00:00",
            "timezone": "UTC",
        },
    )
    event_id = create_response.json()["id"]

    delete_response = authenticated_client.delete(f"/api/events/{event_id}")
    assert delete_response.status_code == 200
    assert called["count"] >= 2
    assert called["deleted"] is True


def test_private_event_sync_only_targets_owner(authenticated_client, monkeypatch):
    """Private event should still trigger sync, but the sync service
    filters recipients internally. Here we just verify sync is called."""
    called = {"events": []}

    class FakeResult:
        users_synced = 1
        events_synced = 1
        errors = []

    def fake_sync(self, event, deleted=False):
        called["events"].append({"visibility": getattr(event, "visibility", "shared"), "deleted": deleted})
        return FakeResult()

    import app.sync.service
    monkeypatch.setattr(app.sync.service.GoogleSyncService, "sync_event_for_household", fake_sync)

    response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Secret dentist",
            "description": None,
            "start_at": "2026-03-18T10:00:00",
            "end_at": "2026-03-18T11:00:00",
            "timezone": "UTC",
            "visibility": "private",
        },
    )
    assert response.status_code == 201
    assert called["events"][0]["visibility"] == "private"


def test_shared_event_sync_targets_all_household(authenticated_client, monkeypatch):
    called = {"events": []}

    class FakeResult:
        users_synced = 2
        events_synced = 1
        errors = []

    def fake_sync(self, event, deleted=False):
        called["events"].append({"visibility": getattr(event, "visibility", "shared")})
        return FakeResult()

    import app.sync.service
    monkeypatch.setattr(app.sync.service.GoogleSyncService, "sync_event_for_household", fake_sync)

    response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Family BBQ",
            "description": None,
            "start_at": "2026-03-18T12:00:00",
            "end_at": "2026-03-18T14:00:00",
            "timezone": "UTC",
            "visibility": "shared",
        },
    )
    assert response.status_code == 201
    assert called["events"][0]["visibility"] == "shared"


# ── Phase 11 Wave 3: Day-click → Sync with reminders (E2E) ───────────────


def test_day_click_entry_syncs_to_google_with_reminders(
    authenticated_client, test_db, test_user_a, monkeypatch,
):
    """E2E: day-click creates event with reminder list → sync payload has overrides."""
    from datetime import datetime, timedelta
    from app.sync.service import GoogleSyncService
    from app.events.repository import EventRepository

    now = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0)

    response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Dentist appointment",
            "description": "Regular checkup",
            "start_at": (now + timedelta(days=7, hours=2)).isoformat(),
            "end_at": (now + timedelta(days=7, hours=3)).isoformat(),
            "timezone": "UTC",
            "reminder_minutes_list": [30, 1440],
        },
    )
    assert response.status_code == 201
    event_data = response.json()
    assert event_data["title"] == "Dentist appointment"
    assert event_data["reminder_minutes_list"] == [30, 1440]

    # Build Google payload via sync service
    service = GoogleSyncService(test_db)
    event = EventRepository(test_db).get_by_id(event_data["id"], test_user_a.calendar_id)
    assert event is not None

    body = service._event_body(event)

    assert body["reminders"]["useDefault"] is False
    overrides = body["reminders"]["overrides"]
    assert len(overrides) == 2
    override_minutes = [o["minutes"] for o in overrides]
    assert 30 in override_minutes
    assert 1440 in override_minutes
    for o in overrides:
        assert o["method"] == "popup"


def test_day_click_entry_with_default_reminders(
    authenticated_client, test_db, test_user_a,
):
    """E2E: day-click event without reminders → Google payload uses useDefault=True."""
    from datetime import datetime, timedelta
    from app.sync.service import GoogleSyncService
    from app.events.repository import EventRepository

    now = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0)

    response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Meeting",
            "start_at": (now + timedelta(hours=3)).isoformat(),
            "end_at": (now + timedelta(hours=4)).isoformat(),
            "timezone": "UTC",
        },
    )
    assert response.status_code == 201

    service = GoogleSyncService(test_db)
    event = EventRepository(test_db).get_by_id(
        response.json()["id"], test_user_a.calendar_id,
    )
    body = service._event_body(event)

    assert body["reminders"]["useDefault"] is True
    assert "overrides" not in body["reminders"] or len(body["reminders"].get("overrides", [])) == 0
