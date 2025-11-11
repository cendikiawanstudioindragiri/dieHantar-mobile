from fastapi.testclient import TestClient


def test_splash_and_capabilities(client: TestClient):
    r = client.get("/config/splash")
    assert r.status_code == 200
    data = r.json()
    assert "image" in data and "duration_ms" in data

    r = client.get("/config/capabilities")
    assert r.status_code == 200
    caps = r.json()
    assert "api_version" in caps and "endpoints" in caps
