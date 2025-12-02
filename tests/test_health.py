from fastapi.testclient import TestClient

from src.api.main import app


def test_live():
    client = TestClient(app)
    res = client.get("/health/live")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
