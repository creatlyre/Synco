import uuid

from app.users.repository import UserRepository


class UserService:
    def __init__(self, db):
        self.db = db
        self.repo = UserRepository(db)

    def _resolve_inviter(
        self,
        inviter_id: str,
        inviter_email: str | None = None,
        inviter_name: str | None = None,
        inviter_external_id: str | None = None,
        auth_token: str | None = None,
    ):
        inviter = self.repo.get_user_by_id(inviter_id, auth_token=auth_token)
        if not inviter:
            inviter = self.repo.get_user_by_external_id(inviter_id, auth_token=auth_token)
        if not inviter and inviter_email:
            inviter = self.repo.get_user_by_email(inviter_email.lower(), auth_token=auth_token)

        if not inviter and inviter_email:
            new_id = str(uuid.uuid4())
            inviter = self.repo.create_user(
                {
                    "id": new_id,
                    "email": inviter_email.lower(),
                    "name": inviter_name or inviter_email,
                    "google_id": inviter_external_id or inviter_id,
                },
                auth_token=auth_token,
            )
            cal = self.repo.create_calendar(
                {
                    "id": str(uuid.uuid4()),
                    "name": f"{(inviter_name or inviter_email)}'s Calendar",
                    "owner_user_id": new_id,
                },
                auth_token=auth_token,
            )
            inviter = self.repo.update_user(
                inviter.id,
                {"calendar_id": cal.id},
                auth_token=auth_token,
            )

        if not inviter:
            raise ValueError("Inviter not found")

        if inviter_external_id and not inviter.google_id:
            inviter = self.repo.update_user(
                inviter.id,
                {"google_id": inviter_external_id},
                auth_token=auth_token,
            ) or inviter

        if not inviter.calendar_id:
            cal = self.repo.create_calendar(
                {
                    "id": str(uuid.uuid4()),
                    "name": f"{inviter.name or inviter.email}'s Calendar",
                    "owner_user_id": inviter.id,
                },
                auth_token=auth_token,
            )
            inviter = self.repo.update_user(inviter.id, {"calendar_id": cal.id}, auth_token=auth_token) or inviter

        return inviter

    def invite_user(
        self,
        inviter_id: str,
        invited_email: str,
        inviter_email: str | None = None,
        inviter_name: str | None = None,
        inviter_external_id: str | None = None,
        auth_token: str | None = None,
    ):
        inviter = self._resolve_inviter(
            inviter_id,
            inviter_email=inviter_email,
            inviter_name=inviter_name,
            inviter_external_id=inviter_external_id,
            auth_token=auth_token,
        )

        normalized_email = invited_email.lower()
        invited_user = self.repo.get_user_by_email(normalized_email, auth_token=auth_token)

        if invited_user and invited_user.calendar_id == inviter.calendar_id:
            raise ValueError(f"{invited_email} is already a member")

        if invited_user and invited_user.calendar_id:
            raise ValueError(f"{invited_email} is already in another household")

        return self.repo.create_invitation(
            inviter.calendar_id,
            normalized_email,
            inviter.id,
            auth_token=auth_token,
        )

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
