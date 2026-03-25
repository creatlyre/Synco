"""Tests for the Synco self-hosted license key system."""

import os

import pytest
from fastapi.testclient import TestClient

from app.licensing.keys import generate_license_key, validate_license_key


# --- Key generation tests ---


class TestGenerateLicenseKey:
    def test_format(self):
        key = generate_license_key("secret")
        assert key.startswith("SYNCO-")
        parts = key.split("-")
        assert len(parts) == 6
        assert parts[0] == "SYNCO"
        for part in parts[1:]:
            assert len(part) == 8, f"Part '{part}' is not 8 chars"

    def test_unique(self):
        k1 = generate_license_key("secret")
        k2 = generate_license_key("secret")
        assert k1 != k2

    def test_deterministic_validation(self):
        secret = "my-secret"
        key = generate_license_key(secret)
        assert validate_license_key(key, secret)


# --- Key validation tests ---


class TestValidateLicenseKey:
    def test_valid_key(self):
        secret = "test-secret-abc"
        key = generate_license_key(secret)
        assert validate_license_key(key, secret) is True

    def test_wrong_secret(self):
        key = generate_license_key("secret-a")
        assert validate_license_key(key, "secret-b") is False

    def test_malformed_random_string(self):
        assert validate_license_key("random-garbage", "secret") is False

    def test_malformed_empty_string(self):
        assert validate_license_key("", "secret") is False

    def test_malformed_synco_prefix_only(self):
        assert validate_license_key("SYNCO-", "secret") is False

    def test_malformed_partial_key(self):
        assert validate_license_key("SYNCO-aabb", "secret") is False

    def test_tampered_key(self):
        secret = "tamper-test"
        key = generate_license_key(secret)
        # Flip the first hex char after SYNCO-
        parts = key.split("-")
        char = parts[1][0]
        flipped = "a" if char != "a" else "b"
        parts[1] = flipped + parts[1][1:]
        tampered = "-".join(parts)
        assert validate_license_key(tampered, secret) is False

    def test_none_key(self):
        assert validate_license_key(None, "secret") is False

    def test_integer_key(self):
        assert validate_license_key(12345, "secret") is False


# --- Middleware tests ---


class TestLicenseCheckMiddleware:
    """Tests for the LicenseCheckMiddleware behavior."""

    def _make_app(self, environment="development", license_key="", license_secret=""):
        """Create a test FastAPI app with LicenseCheckMiddleware."""
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse, JSONResponse
        from app.licensing.middleware import LicenseCheckMiddleware

        test_app = FastAPI()
        test_app.add_middleware(
            LicenseCheckMiddleware,
            environment=environment,
            license_key=license_key,
            license_secret=license_secret,
        )

        @test_app.get("/page", response_class=HTMLResponse)
        async def page():
            return "<html><body><h1>Hello</h1></body></html>"

        @test_app.get("/api/data")
        async def api_data():
            return {"key": "value"}

        @test_app.get("/health")
        async def health():
            return {"status": "ok"}

        @test_app.get("/health/ready")
        async def health_ready():
            return {"status": "ready"}

        return test_app

    def test_skips_non_selfhosted(self):
        app = self._make_app(environment="production")
        client = TestClient(app)
        resp = client.get("/page")
        assert resp.status_code == 200
        assert "Invalid or missing license key" not in resp.text

    def test_valid_key_no_banner(self):
        secret = "test-mw-secret"
        key = generate_license_key(secret)
        app = self._make_app(
            environment="self-hosted", license_key=key, license_secret=secret
        )
        client = TestClient(app)
        resp = client.get("/page")
        assert resp.status_code == 200
        assert "Invalid or missing license key" not in resp.text

    def test_invalid_key_shows_banner(self):
        app = self._make_app(
            environment="self-hosted",
            license_key="SYNCO-bad-key",
            license_secret="secret",
        )
        client = TestClient(app)
        resp = client.get("/page")
        assert resp.status_code == 200
        assert "Invalid or missing license key" in resp.text

    def test_missing_key_shows_banner(self):
        app = self._make_app(
            environment="self-hosted", license_key="", license_secret="secret"
        )
        client = TestClient(app)
        resp = client.get("/page")
        assert resp.status_code == 200
        assert "Invalid or missing license key" in resp.text

    def test_skips_health_endpoints(self):
        app = self._make_app(
            environment="self-hosted", license_key="", license_secret="secret"
        )
        client = TestClient(app)
        resp = client.get("/health")
        assert resp.status_code == 200
        assert "Invalid or missing license key" not in resp.text
        resp2 = client.get("/health/ready")
        assert resp2.status_code == 200
        assert "Invalid or missing license key" not in resp2.text

    def test_skips_api_json(self):
        app = self._make_app(
            environment="self-hosted", license_key="", license_secret="secret"
        )
        client = TestClient(app)
        resp = client.get("/api/data")
        assert resp.status_code == 200
        data = resp.json()
        assert data == {"key": "value"}


# --- Telemetry tests ---

import uuid
from datetime import datetime, timedelta
from unittest.mock import patch
from pathlib import Path

from app.admin.dependencies import get_admin_user
from app.auth.dependencies import get_current_user, get_current_user_optional
from app.database.database import get_db
from app.database.models import Calendar, User
from app.licensing.telemetry import (
    get_or_create_install_id,
    check_integrity,
    build_heartbeat_payload,
    _host_fingerprint,
)
from main import app as main_app
from tests.conftest import InMemoryStore


class TestInstallId:
    def test_creates_valid_uuid(self, tmp_path):
        with patch("app.licensing.telemetry._project_root", return_value=tmp_path):
            install_id = get_or_create_install_id()
            uuid.UUID(install_id)

    def test_persists_across_calls(self, tmp_path):
        with patch("app.licensing.telemetry._project_root", return_value=tmp_path):
            first = get_or_create_install_id()
            second = get_or_create_install_id()
            assert first == second

    def test_regenerates_if_corrupt(self, tmp_path):
        id_file = tmp_path / ".synco_install_id"
        id_file.write_text("not-a-uuid\n")
        with patch("app.licensing.telemetry._project_root", return_value=tmp_path):
            install_id = get_or_create_install_id()
            uuid.UUID(install_id)


class TestIntegrity:
    def test_check_integrity_returns_dict(self):
        result = check_integrity()
        assert "hashes" in result
        assert "ok" in result
        assert isinstance(result["ok"], bool)

    def test_missing_file_makes_integrity_fail(self, tmp_path):
        with patch("app.licensing.telemetry._project_root", return_value=tmp_path):
            result = check_integrity()
            assert result["ok"] is False


class TestHeartbeatPayload:
    def test_payload_contains_required_fields(self):
        payload = build_heartbeat_payload(
            install_id="test-id",
            license_valid=False,
            environment="test",
        )
        assert payload["installation_id"] == "test-id"
        assert payload["license_valid"] is False
        assert payload["environment"] == "test"
        assert "version" in payload
        assert "file_hashes" in payload
        assert "host_fingerprint" in payload
        assert "reported_at" in payload

    def test_host_fingerprint_is_stable(self):
        a = _host_fingerprint()
        b = _host_fingerprint()
        assert a == b
        assert len(a) == 16


# --- API tests: heartbeat receiver & admin endpoints ---


@pytest.fixture
def telemetry_db():
    store = InMemoryStore()
    cal = Calendar(id=str(uuid.uuid4()), name="Admin Cal")
    store.add(cal)
    admin = User(
        id=str(uuid.uuid4()),
        email="admin@test.com",
        name="Admin",
        is_admin=True,
        calendar_id=cal.id,
    )
    store.add(admin)
    return store, admin


@pytest.fixture
def telemetry_client(telemetry_db):
    store, admin = telemetry_db

    def override_get_db():
        yield store

    async def override_admin():
        return admin

    async def override_current():
        return admin

    main_app.dependency_overrides[get_db] = override_get_db
    main_app.dependency_overrides[get_admin_user] = override_admin
    main_app.dependency_overrides[get_current_user] = override_current
    main_app.dependency_overrides[get_current_user_optional] = override_current

    client = TestClient(main_app)
    yield client
    main_app.dependency_overrides.clear()


class TestHeartbeatEndpoint:
    def test_first_heartbeat_creates_record(self, telemetry_client):
        resp = telemetry_client.post("/api/telemetry/heartbeat", json={
            "installation_id": "aaaa-bbbb-cccc",
            "version": "1.0.0",
            "license_valid": True,
            "integrity_ok": True,
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_second_heartbeat_updates_record(self, telemetry_client):
        payload = {
            "installation_id": "aaaa-bbbb-cccc",
            "version": "1.0.0",
            "license_valid": False,
            "integrity_ok": True,
        }
        telemetry_client.post("/api/telemetry/heartbeat", json=payload)
        payload["license_valid"] = True
        telemetry_client.post("/api/telemetry/heartbeat", json=payload)

        resp = telemetry_client.get("/api/admin/installations")
        data = resp.json()
        matching = [i for i in data["installations"] if i["installation_id"] == "aaaa-bbbb-cccc"]
        assert len(matching) == 1
        assert matching[0]["license_valid"] is True

    def test_heartbeat_rejects_empty_install_id(self, telemetry_client):
        resp = telemetry_client.post("/api/telemetry/heartbeat", json={
            "installation_id": "",
        })
        assert resp.status_code == 422


class TestAdminInstallations:
    def test_list_installations(self, telemetry_client, telemetry_db):
        store, _ = telemetry_db
        store.insert("installations", {
            "installation_id": "inst-1",
            "version": "1.0.0",
            "license_valid": True,
            "integrity_ok": True,
            "environment": "production",
        })
        store.insert("installations", {
            "installation_id": "inst-2",
            "version": "1.0.0",
            "license_valid": False,
            "integrity_ok": False,
            "environment": "self-hosted",
        })
        resp = telemetry_client.get("/api/admin/installations")
        data = resp.json()
        assert data["total"] == 2
        assert data["summary"]["licensed"] == 1
        assert data["summary"]["unlicensed"] == 1
        assert data["summary"]["tampered"] == 1

    def test_filter_unlicensed(self, telemetry_client, telemetry_db):
        store, _ = telemetry_db
        store.insert("installations", {"installation_id": "lic-1", "license_valid": True, "integrity_ok": True})
        store.insert("installations", {"installation_id": "unlic-1", "license_valid": False, "integrity_ok": True})
        resp = telemetry_client.get("/api/admin/installations?license_filter=unlicensed")
        ids = [i["installation_id"] for i in resp.json()["installations"]]
        assert "unlic-1" in ids
        assert "lic-1" not in ids

    def test_filter_tampered(self, telemetry_client, telemetry_db):
        store, _ = telemetry_db
        store.insert("installations", {"installation_id": "clean-1", "license_valid": True, "integrity_ok": True})
        store.insert("installations", {"installation_id": "tampered-1", "license_valid": False, "integrity_ok": False})
        resp = telemetry_client.get("/api/admin/installations?integrity_filter=tampered")
        ids = [i["installation_id"] for i in resp.json()["installations"]]
        assert "tampered-1" in ids
        assert "clean-1" not in ids

    def test_stats_endpoint(self, telemetry_client, telemetry_db):
        store, _ = telemetry_db
        store.insert("installations", {"installation_id": "s1", "license_valid": True, "integrity_ok": True})
        resp = telemetry_client.get("/api/admin/installations/stats")
        data = resp.json()
        assert data["total"] == 1
        assert data["licensed"] == 1
