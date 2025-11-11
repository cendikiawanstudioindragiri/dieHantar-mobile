from fastapi.testclient import TestClient


def test_product_list_cache_invalidation(client: TestClient):
    # Create user & login
    client.post("/auth/signup", json={"email": "prod@example.com", "password": "Secret123", "full_name": "Prod User"})
    r = client.post("/auth/login", json={"email": "prod@example.com", "password": "Secret123"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Initial list (empty) - triggers cache set if backend cache available
    r = client.get("/products/")
    assert r.status_code == 200
    assert r.json() == []

    # Create product
    r = client.post(
        "/products/",
        headers=headers,
        json={"name": "Widget", "description": "A widget", "price": 9.99, "available": True},
    )
    assert r.status_code == 201
    prod_id = r.json()["id"]

    # List again should include product (cache invalidated if existed)
    r2 = client.get("/products/")
    assert r2.status_code == 200
    arr = r2.json()
    assert any(p["id"] == prod_id for p in arr)
