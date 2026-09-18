from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
import webapp

client = TestClient(webapp.app)


def test_index_and_static():
    page = client.get("/")
    assert page.status_code == 200
    assert "KA-GZSL" in page.text
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/style.css").status_code == 200


def test_health_has_no_fake_ready_state():
    data = client.get("/api/health").json()
    assert data["video_files_ready"] == (len(data["missing"]) == 0)
    assert data["confidence_kind"] == "relative_softmax_uncalibrated"


def test_post_requires_token():
    assert client.post("/api/sample").status_code == 403


def test_unsupported_file():
    token = client.get("/api/health").json()["server_token"]
    response = client.post("/api/jobs", headers={"x-ka-demo-token": token}, files={"file": ("model.pt", b"bad")})
    assert response.status_code == 415


def test_invalid_mode():
    token = client.get("/api/health").json()["server_token"]
    response = client.post("/api/jobs", headers={"x-ka-demo-token": token},
                           files={"file": ("clip.mp4", b"bad")}, data={"mode": "anything"})
    assert response.status_code == 422


def test_missing_assets_fail_closed(monkeypatch):
    monkeypatch.setattr(webapp, "readiness", lambda _: {"video_files_ready": False, "missing": ["WavCaps"]})
    response = client.post("/api/jobs", headers={"x-ka-demo-token": webapp.TOKEN}, files={"file": ("clip.mp4", b"bad")})
    assert response.status_code == 503
    assert "WavCaps" in response.json()["detail"]


def test_path_traversal_and_foreign_host():
    assert client.get("/api/jobs/not-a-uuid").status_code == 404
    assert client.get("/api/health", headers={"host": "attacker.example"}).status_code == 403


def test_declared_oversize_rejected():
    response = client.post("/api/jobs", content=b"x", headers={"content-length": str(1024 ** 3)})
    assert response.status_code == 413
