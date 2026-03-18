from typing import Optional

import jwt
from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User
from config import Settings


async def get_current_user(
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db),
) -> User:
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    settings = Settings()
    try:
        payload = jwt.decode(session, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Session expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid session") from exc

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
