from app.data.ids import DEMO_USER_ID


def test_profile_without_auth_uses_demo_user(client):
    response = client.get("/api/v1/profile")
    assert response.status_code == 200
    assert response.json()["id"] == DEMO_USER_ID


def test_bearer_token_ignored_when_supabase_disabled(client):
    response = client.get("/api/v1/profile", headers={"Authorization": "Bearer whatever"})
    assert response.status_code == 200
    assert response.json()["id"] == DEMO_USER_ID


def test_invalid_supabase_session_is_rejected(client, monkeypatch):
    monkeypatch.setattr("app.auth.settings.supabase_url", "https://example.supabase.co")
    monkeypatch.setattr("app.auth.settings.supabase_service_role_key", "test-key")

    class FakeResponse:
        status_code = 401

        def json(self):
            return {}

    monkeypatch.setattr("app.auth.httpx.get", lambda *_args, **_kwargs: FakeResponse())
    response = client.get("/api/v1/profile", headers={"Authorization": "Bearer bad-token"})
    assert response.status_code == 401


def test_valid_supabase_session_uses_user_id(client, monkeypatch):
    monkeypatch.setattr("app.auth.settings.supabase_url", "https://example.supabase.co")
    monkeypatch.setattr("app.auth.settings.supabase_service_role_key", "test-key")
    user_id = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"

    class FakeResponse:
        status_code = 200

        def json(self):
            return {"id": user_id}

    monkeypatch.setattr("app.auth.httpx.get", lambda *_args, **_kwargs: FakeResponse())
    response = client.get("/api/v1/profile", headers={"Authorization": "Bearer good-token"})
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert {skill["slug"] for skill in response.json()["skills"]} == {
        "screen_swap",
        "battery_replacement",
    }
