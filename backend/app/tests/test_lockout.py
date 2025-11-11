from fastapi.testclient import TestClient


def test_login_lockout_and_reset(client: TestClient):
    # Create a user
    r = client.post(
        "/auth/signup",
        json={"email": "lock@example.com", "password": "Secret123", "full_name": "Lock Tester"},
    )
    assert r.status_code == 200, r.text

    # Wrong password attempts up to MAX_LOGIN_ATTEMPTS
    attempts = 5  # default MAX_LOGIN_ATTEMPTS in settings
    for _ in range(attempts):
        r = client.post("/auth/login", json={"email": "lock@example.com", "password": "wrong"})
        assert r.status_code == 401

    # Next attempt should be locked out (429)
    r = client.post("/auth/login", json={"email": "lock@example.com", "password": "wrong"})
    assert r.status_code == 429

    # Reset lockout manually (simulate window expiry)
    from app.core.security import reset_failed_login

    reset_failed_login("login:lock@example.com")

    # Correct login should succeed after reset
    r = client.post("/auth/login", json={"email": "lock@example.com", "password": "Secret123"})
    assert r.status_code == 200, r.text
    assert r.json().get("access_token")
