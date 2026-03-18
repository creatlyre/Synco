from datetime import datetime, timedelta
import uuid

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.oauth import exchange_code_for_token, get_authorization_url
from app.auth.utils import encrypt_token
from app.database.database import get_db
from app.database.models import Calendar, User
from app.users.service import UserService
from config import Settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login():
    auth_url, _state = get_authorization_url()
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def oauth_callback(code: str, state: str, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="Missing auth code")

    try:
        tokens = exchange_code_for_token(code, state)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {exc}") from exc

    user_info = tokens["user_info"]
    if not user_info.get("email") or not user_info.get("google_id"):
        raise HTTPException(status_code=400, detail="Google profile data is incomplete")

    user = db.query(User).filter(User.google_id == user_info["google_id"]).first()

    if not user:
        user = User(
            id=str(uuid.uuid4()),
            email=user_info["email"].lower(),
            name=user_info.get("name") or user_info["email"],
            google_id=user_info["google_id"],
            google_access_token=encrypt_token(tokens["access_token"]),
            google_refresh_token=encrypt_token(tokens.get("refresh_token") or ""),
            google_token_expiry=tokens["token_expiry"],
            last_login=datetime.utcnow(),
        )

        calendar = Calendar(
            id=str(uuid.uuid4()),
            name=f"{user.name}'s Calendar",
            owner_user_id=user.id,
        )
        user.calendar_id = calendar.id

        db.add(calendar)
        db.add(user)
    else:
        user.google_access_token = encrypt_token(tokens["access_token"])
        if tokens.get("refresh_token"):
            user.google_refresh_token = encrypt_token(tokens["refresh_token"])
        user.google_token_expiry = tokens["token_expiry"]
        user.last_login = datetime.utcnow()
        db.add(user)

    db.commit()
    db.refresh(user)

    # Auto-accept pending household invitations after login.
    service = UserService(db)
    service.accept_household_invitation(user.id)

    settings = Settings()
    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRY_HOURS),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.JWT_EXPIRY_HOURS * 3600,
    )
    return response


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out"}
