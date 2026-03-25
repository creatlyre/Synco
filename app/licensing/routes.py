"""API endpoint that receives telemetry heartbeats from Synco installations
and an admin-only endpoint for viewing tracked installations."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.admin.dependencies import get_admin_user
from app.database.database import get_db

router = APIRouter(tags=["telemetry"])


# ── Heartbeat receiver (public — called by remote installations) ──────────

class HeartbeatPayload(BaseModel):
    installation_id: str = Field(..., min_length=1, max_length=64)
    version: str = Field(default="unknown", max_length=32)
    environment: str = Field(default="unknown", max_length=32)
    license_valid: bool = False
    integrity_ok: bool = True
    file_hashes: dict[str, str | None] = Field(default_factory=dict)
    host_fingerprint: str = Field(default="", max_length=64)
    python_version: str = Field(default="", max_length=32)
    os: str = Field(default="", max_length=32)
    reported_at: str | None = None


@router.post("/api/telemetry/heartbeat")
async def receive_heartbeat(payload: HeartbeatPayload, db=Depends(get_db)):
    """Upsert an installation record from a remote heartbeat."""
    now = datetime.now(timezone.utc).isoformat()
    row = {
        "installation_id": payload.installation_id,
        "version": payload.version,
        "environment": payload.environment,
        "license_valid": payload.license_valid,
        "integrity_ok": payload.integrity_ok,
        "file_hashes": payload.file_hashes,
        "host_fingerprint": payload.host_fingerprint,
        "python_version": payload.python_version,
        "os": payload.os,
        "reported_at": payload.reported_at or now,
        "updated_at": now,
    }

    # Try update first (existing installation)
    existing = db.select(
        "installations",
        {"installation_id": f"eq.{payload.installation_id}", "limit": "1"},
    )
    if existing:
        db.update(
            "installations",
            {"installation_id": f"eq.{payload.installation_id}"},
            row,
        )
    else:
        row["created_at"] = now
        db.insert("installations", row)

    return {"status": "ok"}


# ── Admin endpoints ──────────────────────────────────────────────────────

@router.get("/api/admin/installations")
async def list_installations(
    admin=Depends(get_admin_user),
    db=Depends(get_db),
    license_filter: str | None = None,
    integrity_filter: str | None = None,
):
    """List all tracked installations (admin only)."""
    params: dict[str, str] = {"order": "updated_at.desc"}
    if license_filter == "unlicensed":
        params["license_valid"] = "eq.false"
    elif license_filter == "licensed":
        params["license_valid"] = "eq.true"
    if integrity_filter == "tampered":
        params["integrity_ok"] = "eq.false"
    elif integrity_filter == "clean":
        params["integrity_ok"] = "eq.true"

    rows = db.select("installations", params)
    return {
        "installations": rows,
        "total": len(rows),
        "summary": _build_summary(rows),
    }


@router.get("/api/admin/installations/stats")
async def installation_stats(
    admin=Depends(get_admin_user),
    db=Depends(get_db),
):
    """Aggregate stats for the admin dashboard card."""
    rows = db.select("installations", {})
    return _build_summary(rows)


def _build_summary(rows: list[dict]) -> dict:
    total = len(rows)
    licensed = sum(1 for r in rows if r.get("license_valid"))
    unlicensed = total - licensed
    tampered = sum(1 for r in rows if not r.get("integrity_ok"))
    return {
        "total": total,
        "licensed": licensed,
        "unlicensed": unlicensed,
        "tampered": tampered,
    }
