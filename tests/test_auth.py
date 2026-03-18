from datetime import datetime

from app.database.models import User


def test_oauth_callback_creates_user(test_db, test_client, monkeypatch):
    def mock_exchange_code_for_token(code: str, state: str):
        return {
            "access_token": "fake_access",
            "refresh_token": "fake_refresh",
            "token_expiry": datetime.utcnow(),
            "user_info": {
                "email": "newuser@example.com",
                "name": "New User",
                "google_id": "google_new",
            },
        }

    import app.auth.routes

    monkeypatch.setattr(app.auth.routes, "exchange_code_for_token", mock_exchange_code_for_token)

    response = test_client.get("/auth/callback?code=fake&state=fake", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers.get("location") == "/"
    assert "session=" in response.headers.get("set-cookie", "")

    user = test_db.query(User).filter(User.email == "newuser@example.com").first()
    assert user is not None
    assert user.calendar_id is not None


def test_invalid_session_redirects(test_client):
    response = test_client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers.get("location") == "/auth/login"
