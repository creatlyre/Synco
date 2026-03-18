from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.database.models import Calendar, CalendarInvitation, User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email.lower()).first()

    def create_invitation(self, calendar_id: str, invited_email: str, inviter_user_id: str) -> CalendarInvitation:
        invitation = CalendarInvitation(
            calendar_id=calendar_id,
            invited_email=invited_email.lower(),
            inviter_user_id=inviter_user_id,
            status="pending",
        )
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        return invitation

    def get_pending_invitations(self, email: str) -> list[CalendarInvitation]:
        return (
            self.db.query(CalendarInvitation)
            .filter(
                and_(
                    CalendarInvitation.invited_email == email.lower(),
                    CalendarInvitation.status == "pending",
                )
            )
            .order_by(CalendarInvitation.created_at.asc())
            .all()
        )

    def accept_invitation(self, invitation_id: str, user_id: str) -> User | None:
        invitation = self.db.query(CalendarInvitation).filter(CalendarInvitation.id == invitation_id).first()
        user = self.db.query(User).filter(User.id == user_id).first()

        if not invitation or not user:
            return None

        user.calendar_id = invitation.calendar_id
        invitation.status = "accepted"
        self.db.add(user)
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_household_members(self, user_id: str) -> list[User]:
        user = self.get_user_by_id(user_id)
        if not user or not user.calendar_id:
            return []

        return self.db.query(User).filter(User.calendar_id == user.calendar_id).all()

    def get_household_calendar(self, user_id: str) -> Calendar | None:
        user = self.get_user_by_id(user_id)
        if not user or not user.calendar_id:
            return None

        return self.db.query(Calendar).filter(Calendar.id == user.calendar_id).first()
