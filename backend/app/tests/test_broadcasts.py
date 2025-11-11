from fastapi.testclient import TestClient


def auth_headers(client: TestClient):
    client.post("/auth/signup", json={"email": "admin@example.com", "password": "Secret123", "full_name": "Admin"})
    r = client.post("/auth/login", json={"email": "admin@example.com", "password": "Secret123"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_broadcast_create_preview_send(client: TestClient):
    headers = auth_headers(client)

    # Create
    r = client.post(
        "/admin/broadcasts/",
        headers=headers,
        json={"title": "Info", "body": "Halo pengguna!", "segment": "all"},
    )
    assert r.status_code == 201, r.text
    bid = r.json()["id"]

    # Preview
    r = client.get(f"/admin/broadcasts/{bid}/preview", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == bid
    assert "estimated_targets" in r.json()

    # Send (dry run)
    r = client.post(f"/admin/broadcasts/{bid}/send", headers=headers, json={"dry_run": True})
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == bid
    assert body["dry_run"] is True
    assert body["success"] >= 1  # at least the admin user exists
