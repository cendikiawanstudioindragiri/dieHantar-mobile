from fastapi.testclient import TestClient


def test_signup_login_me(client: TestClient):
    # Sign up
    r = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "secret1", "full_name": "Tester"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["email"] == "test@example.com"
    assert data.get("id") is not None

    # Login
    r = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "secret1"}
    )
    assert r.status_code == 200, r.text
    token = r.json().get("access_token")
    assert token and isinstance(token, str)

    # /me
    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    me = r.json()
    assert me["email"] == "test@example.com"


def test_categories_list_and_create(client: TestClient):
    # Ensure list is empty at start
    r = client.get("/categories/")
    assert r.status_code == 200, r.text
    assert isinstance(r.json(), list)
    assert len(r.json()) == 0

    # Create a user and login to post category
    client.post(
        "/auth/signup",
        json={"email": "catadmin@example.com", "password": "secret1", "full_name": "Cat Admin"},
    )
    r = client.post(
        "/auth/login", json={"email": "catadmin@example.com", "password": "secret1"}
    )
    token = r.json()["access_token"]

    # Create category
    r = client.post(
        "/categories/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Beverages"},
    )
    assert r.status_code == 201, r.text
    cat = r.json()
    assert cat["name"] == "Beverages"

    # Duplicate should 400
    r_dup = client.post(
        "/categories/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Beverages"},
    )
    assert r_dup.status_code == 400

    # List now has one
    r = client.get("/categories/")
    assert r.status_code == 200, r.text
    arr = r.json()
    assert len(arr) == 1
    assert arr[0]["name"] == "Beverages"
