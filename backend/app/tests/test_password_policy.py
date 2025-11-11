from fastapi.testclient import TestClient


def test_signup_password_policy(client: TestClient):
    # weak password (no digit)
    r = client.post(
        "/auth/signup",
        json={"email": "weak1@example.com", "password": "abcdef", "full_name": "Weak"},
    )
    assert r.status_code == 400

    # weak password (too short)
    r = client.post(
        "/auth/signup",
        json={"email": "weak2@example.com", "password": "a1", "full_name": "Weak"},
    )
    assert r.status_code == 400

    # strong password
    r = client.post(
        "/auth/signup",
        json={"email": "strong@example.com", "password": "abc12345", "full_name": "Strong"},
    )
    assert r.status_code == 200
