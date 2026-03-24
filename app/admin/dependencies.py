from fastapi import Depends, HTTPException

from app.auth.dependencies import get_current_user


async def get_admin_user(user=Depends(get_current_user)):
    if not getattr(user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
