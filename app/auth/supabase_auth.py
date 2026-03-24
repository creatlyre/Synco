from __future__ import annotations

from typing import Any, Dict, Optional
from urllib.parse import urlencode

import httpx
import jwt

from config import Settings


def is_supabase_auth_enabled(settings: Settings | None = None) -> bool:
    settings = settings or Settings()
    return bool(settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY)


def build_google_authorize_url(redirect_to: str) -> str:
    settings = Settings()
    base = settings.SUPABASE_URL.rstrip("/")
    scope_value = " ".join(settings.GOOGLE_SCOPES)
    query = urlencode(
        {
            "provider": "google",
            "redirect_to": redirect_to,
            "scopes": scope_value,
            "prompt": "consent",
            "access_type": "offline",
            "include_granted_scopes": "true",
        }
    )
    return f"{base}/auth/v1/authorize?{query}"


async def fetch_supabase_user(access_token: str) -> Optional[Dict[str, Any]]:
    settings = Settings()
    if not is_supabase_auth_enabled(settings):
        return None

    base = settings.SUPABASE_URL.rstrip("/")
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {access_token}",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{base}/auth/v1/user", headers=headers)
    if response.status_code != 200:
        return None
    return response.json()


def decode_legacy_session_token(session_token: str) -> Optional[Dict[str, Any]]:
    settings = Settings()
    try:
        return jwt.decode(session_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        return None


async def is_valid_session_token(session_token: str) -> bool:
    if decode_legacy_session_token(session_token):
        return True
    user = await fetch_supabase_user(session_token)
    return bool(user)


async def supabase_sign_up(email: str, password: str) -> Dict[str, Any]:
    settings = Settings()
    base = settings.SUPABASE_URL.rstrip("/")
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }
    payload = {"email": email, "password": password}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(f"{base}/auth/v1/signup", json=payload, headers=headers)

    data = response.json()
    if response.status_code >= 400:
        message = data.get("msg") or data.get("error_description") or data.get("error") or "Signup failed"
        raise ValueError(message)
    return data


async def supabase_password_sign_in(email: str, password: str) -> Dict[str, Any]:
    settings = Settings()
    base = settings.SUPABASE_URL.rstrip("/")
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }
    payload = {"email": email, "password": password}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            f"{base}/auth/v1/token?grant_type=password",
            json=payload,
            headers=headers,
        )

    data = response.json()
    if response.status_code >= 400:
        message = data.get("msg") or data.get("error_description") or data.get("error") or "Sign-in failed"
        raise ValueError(message)
    return data


async def refresh_supabase_access_token(refresh_token: str) -> Optional[Dict[str, Any]]:
    settings = Settings()
    if not is_supabase_auth_enabled(settings):
        return None

    base = settings.SUPABASE_URL.rstrip("/")
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    form_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            f"{base}/auth/v1/token",
            params={"grant_type": "refresh_token"},
            data=form_data,
            headers=headers,
        )

    if response.status_code >= 400:
        return None

    data = response.json()
    if not data.get("access_token"):
        return None
    return data


async def supabase_request_password_reset(email: str, redirect_to: str) -> Dict[str, Any]:
    """Request Supabase to send a password recovery email."""
    settings = Settings()
    base = settings.SUPABASE_URL.rstrip("/")
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {"email": email}
    if redirect_to:
        payload["redirect_to"] = redirect_to
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(f"{base}/auth/v1/recover", json=payload, headers=headers)
    if response.status_code >= 400:
        data = response.json()
        message = data.get("msg") or data.get("error_description") or data.get("error") or "Password reset failed"
        raise ValueError(message)
    return response.json() if response.text else {}


async def supabase_verify_otp(token_hash: str, type_: str) -> Dict[str, Any]:
    """Exchange a Supabase OTP token_hash for a session (signup confirmation or recovery)."""
    settings = Settings()
    base = settings.SUPABASE_URL.rstrip("/")
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }
    payload = {"token_hash": token_hash, "type": type_}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(f"{base}/auth/v1/verify", json=payload, headers=headers)
    data = response.json()
    if response.status_code >= 400:
        message = data.get("msg") or data.get("error_description") or data.get("error") or "Verification failed"
        raise ValueError(message)
    return data


async def supabase_update_user_password(access_token: str, new_password: str) -> Dict[str, Any]:
    """Update the authenticated user's password."""
    settings = Settings()
    base = settings.SUPABASE_URL.rstrip("/")
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"password": new_password}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.put(f"{base}/auth/v1/user", json=payload, headers=headers)
    data = response.json()
    if response.status_code >= 400:
        message = data.get("msg") or data.get("error_description") or data.get("error") or "Password update failed"
        raise ValueError(message)
    return data