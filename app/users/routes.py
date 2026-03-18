from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.users.service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


class InviteRequest(BaseModel):
    email: EmailStr


class InvitationResponse(BaseModel):
    message: str
    invited_email: str


@router.get("/me")
async def get_current_user_info(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "calendar_id": user.calendar_id,
        "last_login": user.last_login,
    }


@router.get("/household")
async def get_household_info(user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    info = service.get_household_info(user.id)

    return {
        "calendar_id": info["calendar"].id if info["calendar"] else None,
        "calendar_name": info["calendar"].name if info["calendar"] else None,
        "member_count": info["member_count"],
        "members": [{"id": m.id, "email": m.email, "name": m.name} for m in info["members"]],
    }


@router.post("/invite", response_model=InvitationResponse)
async def invite_household_member(
    request: InviteRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if request.email.lower() == user.email.lower():
        raise HTTPException(status_code=400, detail="Cannot invite yourself")

    service = UserService(db)
    try:
        invitation = service.invite_user(user.id, request.email)
        return InvitationResponse(
            message=f"Invitation sent to {request.email}",
            invited_email=invitation.invited_email,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/accept-invitation")
async def accept_invitation(user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    result = service.accept_household_invitation(user.id)

    if result:
        return {"message": "Invitation accepted", "calendar_id": result.calendar_id}
    return {"message": "No pending invitations"}
