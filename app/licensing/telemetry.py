"""Installation telemetry for Synco license compliance tracking.

Generates a persistent installation fingerprint and periodically reports
anonymised deployment data (installation ID, version, license status,
integrity check results) to the Synco telemetry endpoint.

All data is non-PII.  The AGPL-3.0 license requires source disclosure for
network deployments — this module helps detect non-compliant installations.
"""

from __future__ import annotations

import hashlib
import logging
import os
import platform
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_INSTALL_ID_FILE = ".synco_install_id"

# Critical files whose integrity we want to verify.  Paths are relative to
# the project root (same directory as main.py).
_CRITICAL_FILES = (
    "app/licensing/middleware.py",
    "app/licensing/keys.py",
    "main.py",
    "LICENSE",
)

_VERSION = "1.0.0"

# ── helpers ──────────────────────────────────────────────────────────────

def _project_root() -> Path:
    """Return the project root (parent of app/)."""
    return Path(__file__).resolve().parent.parent.parent


def get_or_create_install_id() -> str:
    """Return a persistent installation UUID, creating one if needed."""
    id_path = _project_root() / _INSTALL_ID_FILE
    try:
        if id_path.exists():
            stored = id_path.read_text().strip()
            # basic validity check
            uuid.UUID(stored)
            return stored
    except (ValueError, OSError):
        pass

    new_id = str(uuid.uuid4())
    try:
        id_path.write_text(new_id + "\n")
    except OSError:
        logger.debug("Could not persist installation id to disk")
    return new_id


def compute_file_hash(path: Path) -> str | None:
    """SHA-256 hex digest of a file, or None if unreadable."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def check_integrity() -> dict[str, Any]:
    """Hash critical project files and return an integrity report.

    Returns a dict with:
      hashes   – {relative_path: sha256 | null}
      ok       – True when *all* critical files are present and readable
    """
    root = _project_root()
    hashes: dict[str, str | None] = {}
    all_ok = True
    for rel in _CRITICAL_FILES:
        h = compute_file_hash(root / rel)
        hashes[rel] = h
        if h is None:
            all_ok = False
    return {"hashes": hashes, "ok": all_ok}


def _host_fingerprint() -> str:
    """One-way hash of hostname + machine id — no PII leaks."""
    raw = f"{platform.node()}:{platform.machine()}:{platform.system()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ── payload ──────────────────────────────────────────────────────────────

def build_heartbeat_payload(
    *,
    install_id: str,
    license_valid: bool,
    environment: str,
) -> dict[str, Any]:
    integrity = check_integrity()
    return {
        "installation_id": install_id,
        "version": _VERSION,
        "environment": environment,
        "license_valid": license_valid,
        "integrity_ok": integrity["ok"],
        "file_hashes": integrity["hashes"],
        "host_fingerprint": _host_fingerprint(),
        "python_version": platform.python_version(),
        "os": platform.system(),
        "reported_at": datetime.now(timezone.utc).isoformat(),
    }


# ── sender ───────────────────────────────────────────────────────────────

def send_heartbeat(
    endpoint: str,
    payload: dict[str, Any],
    *,
    timeout: float = 10.0,
) -> bool:
    """POST the heartbeat payload to *endpoint*.  Returns True on success."""
    if not endpoint:
        logger.debug("Telemetry endpoint not configured — skipping heartbeat")
        return False
    try:
        resp = httpx.post(endpoint, json=payload, timeout=timeout)
        if resp.status_code < 300:
            logger.info("Telemetry heartbeat sent (install=%s)", payload.get("installation_id", "")[:8])
            return True
        logger.warning("Telemetry endpoint returned %s", resp.status_code)
    except httpx.HTTPError as exc:
        logger.warning("Telemetry heartbeat failed: %s", exc)
    return False


def send_heartbeat_async(endpoint: str, payload: dict[str, Any]) -> None:
    """Fire-and-forget heartbeat in a daemon thread — never blocks startup."""
    t = threading.Thread(target=send_heartbeat, args=(endpoint, payload), daemon=True)
    t.start()


# ── periodic background reporter ─────────────────────────────────────────

class TelemetryReporter:
    """Sends a heartbeat on start and then every *interval* seconds."""

    def __init__(
        self,
        endpoint: str,
        install_id: str,
        license_valid: bool,
        environment: str,
        interval: int = 86_400,  # default: once per day
    ):
        self.endpoint = endpoint
        self.install_id = install_id
        self.license_valid = license_valid
        self.environment = environment
        self.interval = interval
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def _loop(self) -> None:
        while not self._stop.is_set():
            payload = build_heartbeat_payload(
                install_id=self.install_id,
                license_valid=self.license_valid,
                environment=self.environment,
            )
            send_heartbeat(self.endpoint, payload)
            self._stop.wait(self.interval)

    def start(self) -> None:
        if not self.endpoint:
            return
        self._thread = threading.Thread(target=self._loop, daemon=True, name="synco-telemetry")
        self._thread.start()
        logger.info("Telemetry reporter started (interval=%ds)", self.interval)

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)
