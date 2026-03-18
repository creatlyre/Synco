from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

from config import Settings


def _get_client_config() -> Dict[str, Any]:
    settings = Settings()
    return {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
        }
    }


def get_flow() -> Flow:
    settings = Settings()
    flow = Flow.from_client_config(
        client_config=_get_client_config(),
        scopes=settings.GOOGLE_SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )
    return flow


def get_authorization_url() -> tuple[str, str]:
    flow = get_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return auth_url, state


def exchange_code_for_token(code: str, state: str) -> Dict[str, Any]:
    flow = get_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials

    id_token = credentials.id_token or {}
    user_info = {
        "email": id_token.get("email", ""),
        "name": id_token.get("name", ""),
        "google_id": id_token.get("sub", ""),
    }

    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_expiry": credentials.expiry or datetime.utcnow(),
        "user_info": user_info,
    }


def refresh_access_token(refresh_token: str) -> Dict[str, Any] | None:
    settings = Settings()
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=settings.GOOGLE_SCOPES,
    )
    try:
        creds.refresh(Request())
        return {
            "access_token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_expiry": creds.expiry,
        }
    except Exception as exc:
        if "invalid_grant" in str(exc):
            return None
        raise
