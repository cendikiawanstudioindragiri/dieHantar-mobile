from fastapi.testclient import TestClient


def auth_headers(client: TestClient):
    client.post("/auth/signup", json={"email": "wallet@example.com", "password": "Secret123", "full_name": "Wallet"})
    r = client.post("/auth/login", json={"email": "wallet@example.com", "password": "Secret123"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_wallet_topup_and_withdraw(client: TestClient):
    headers = auth_headers(client)

    # initial balance
    r = client.get("/wallet/balance", headers=headers)
    assert r.status_code == 200
    assert r.json()["balance"] == 0

    # topup
    r = client.post("/wallet/topup", headers=headers, json={"amount": 50})
    assert r.status_code == 201
    assert r.json()["balance"] == 50

    # withdraw partial
    r = client.post("/wallet/withdraw", headers=headers, json={"amount": 20})
    assert r.status_code == 200
    assert r.json()["balance"] == 30

    # insufficient funds
    r = client.post("/wallet/withdraw", headers=headers, json={"amount": 100})
    assert r.status_code == 400
    body = r.json()
    assert body["error"]["code"] == 400
    assert "Insufficient" in body["error"]["message"]

    # transactions list
    r = client.get("/wallet/transactions", headers=headers)
    assert r.status_code == 200
    arr = r.json()
    # Expect 2 transactions: TOPUP then WITHDRAW (failed withdraw doesn't create tx)
    assert len(arr) >= 2
    types = [t["type"] for t in arr]
    assert "TOPUP" in types and "WITHDRAW" in types
