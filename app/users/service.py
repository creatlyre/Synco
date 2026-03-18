from sqlalchemy.orm import Session

from app.users.repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def invite_user(self, inviter_id: str, invited_email: str):
        inviter = self.repo.get_user_by_id(inviter_id)
        if not inviter or not inviter.calendar_id:
            raise ValueError("Inviter has no calendar")

        normalized_email = invited_email.lower()
        invited_user = self.repo.get_user_by_email(normalized_email)

        if invited_user and invited_user.calendar_id == inviter.calendar_id:
            raise ValueError(f"{invited_email} is already a member")

        if invited_user and invited_user.calendar_id:
            raise ValueError(f"{invited_email} is already in another household")

        return self.repo.create_invitation(inviter.calendar_id, normalized_email, inviter_id)

    def accept_household_invitation(self, user_id: str):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        pending = self.repo.get_pending_invitations(user.email)
        if not pending:
            return None

        return self.repo.accept_invitation(pending[0].id, user_id)

    def get_household_info(self, user_id: str) -> dict:
        calendar = self.repo.get_household_calendar(user_id)
        members = self.repo.get_household_members(user_id)

        return {
            "calendar": calendar,
            "members": members,
            "member_count": len(members),
        }
