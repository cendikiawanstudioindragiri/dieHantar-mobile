from fastapi.testclient import TestClient


def test_structured_error_duplicate_category(client: TestClient):
    # signup + login
    client.post("/auth/signup", json={"email": "errfmt@example.com", "password": "Secret123", "full_name": "Err Fmt"})
    r = client.post("/auth/login", json={"email": "errfmt@example.com", "password": "Secret123"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create category
    r1 = client.post("/categories/", headers=headers, json={"name": "Snacks"})
    assert r1.status_code == 201

    # duplicate -> expect structured error
    r2 = client.post("/categories/", headers=headers, json={"name": "Snacks"})
    assert r2.status_code == 400
    body = r2.json()
    assert "error" in body
    assert body["error"]["code"] == 400
    assert isinstance(body["error"]["message"], str)


def test_structured_error_not_found(client: TestClient):
    r = client.get("/products/99999")
    assert r.status_code == 404
    body = r.json()
    assert body["error"]["code"] == 404
    assert body["error"]["message"] == "Product not found"
