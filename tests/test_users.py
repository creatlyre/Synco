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
    saved_rows = test_db.select("calendar_invitations", {"id": f"eq.{invitation.id}", "limit": "1"})
    saved_invite = CalendarInvitation(**saved_rows[0]) if saved_rows else None
    assert saved_invite is not None
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


def test_invite_user_resolves_inviter_by_email_when_id_is_external(test_db, test_user_a, test_user_b):
    service = UserService(test_db)

    invitation = service.invite_user(
        inviter_id="supabase-external-id-123",
        invited_email=test_user_b.email,
        inviter_email=test_user_a.email,
        inviter_name=test_user_a.name,
    )

    assert invitation.status == "pending"
    assert invitation.invited_email == test_user_b.email
    assert invitation.inviter_user_id == test_user_a.id


def test_invite_user_resolves_inviter_by_external_id(test_db, test_user_a, test_user_b):
    service = UserService(test_db)
    test_db.update("users", {"id": f"eq.{test_user_a.id}"}, {"google_id": "supabase-external-id-456"})

    invitation = service.invite_user(
        inviter_id="supabase-external-id-456",
        invited_email=test_user_b.email,
    )

    assert invitation.status == "pending"
    assert invitation.invited_email == test_user_b.email
    assert invitation.inviter_user_id == test_user_a.id


def test_invite_user_includes_explicit_invitation_id_in_insert_payload(test_db, test_user_a, test_user_b, monkeypatch):
    service = UserService(test_db)
    original_insert = test_db.insert
    captured_payload: dict[str, object] = {}

    def tracking_insert(table: str, payload: dict[str, object], auth_token=None):
        if table == "calendar_invitations":
            captured_payload.update(payload)
        return original_insert(table, payload, auth_token)

    monkeypatch.setattr(test_db, "insert", tracking_insert)

    invitation = service.invite_user(test_user_a.id, test_user_b.email)

    assert "id" in captured_payload
    assert isinstance(captured_payload["id"], str)
    assert captured_payload["id"]
    assert invitation.id == captured_payload["id"]
