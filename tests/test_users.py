import pytest

from app.database.models import CalendarInvitation
from app.users.service import UserService


def test_invite_user(test_db, test_user_a, test_user_b):
    service = UserService(test_db)
    invitation = service.invite_user(test_user_a.id, test_user_b.email)

    assert invitation.status == "pending"
    assert invitation.invited_email == test_user_b.email
    assert invitation.calendar_id == test_user_a.calendar_id


def test_accept_invitation(test_db, test_user_a, test_user_b):
    service = UserService(test_db)
    invitation = service.invite_user(test_user_a.id, test_user_b.email)

    result = service.accept_household_invitation(test_user_b.id)

    assert result.calendar_id == test_user_a.calendar_id
    saved_invite = test_db.query(CalendarInvitation).filter_by(id=invitation.id).first()
    assert saved_invite.status == "accepted"


def test_both_users_see_same_calendar(test_db, test_user_a, test_user_b):
    service = UserService(test_db)

    service.invite_user(test_user_a.id, test_user_b.email)
    service.accept_household_invitation(test_user_b.id)
    test_db.refresh(test_user_b)

    assert test_user_a.calendar_id == test_user_b.calendar_id

    info_a = service.get_household_info(test_user_a.id)
    info_b = service.get_household_info(test_user_b.id)

    assert info_a["member_count"] == 2
    assert info_b["member_count"] == 2


def test_cannot_invite_twice(test_db, test_user_a, test_user_b):
    service = UserService(test_db)

    service.invite_user(test_user_a.id, test_user_b.email)
    service.accept_household_invitation(test_user_b.id)

    with pytest.raises(ValueError, match="already a member"):
        service.invite_user(test_user_a.id, test_user_b.email)
