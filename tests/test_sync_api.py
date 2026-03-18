from datetime import datetime


def test_sync_status(authenticated_client):
    response = authenticated_client.get("/api/sync/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_export_month_uses_service(authenticated_client, monkeypatch):
    called = {"ok": False}

    class FakeResult:
        users_synced = 2
        events_synced = 3
        errors = []

    def fake_export_month(self, user, year, month):
        called["ok"] = True
        assert year == 2026
        assert month == 3
        return FakeResult()

    import app.sync.service

    monkeypatch.setattr(app.sync.service.GoogleSyncService, "export_month", fake_export_month)

    response = authenticated_client.post("/api/sync/export-month?year=2026&month=3")
    assert response.status_code == 200
    data = response.json()
    assert data["users_synced"] == 2
    assert data["events_synced"] == 3
    assert called["ok"]
