import os
import sys
import types

# Make 'flask_app' importable by inserting workspace root and ensuring package
root = "/workspaces/dieHantar-mobile"
if root not in sys.path:
    sys.path.insert(0, root)

from flask_app import create_app


def test_health_version():
    os.environ["APP_VERSION"] = "1.2.3-test"
    app = create_app()
    client = app.test_client()
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["version"] == "1.2.3-test"
    assert data["status"] == "ok"
