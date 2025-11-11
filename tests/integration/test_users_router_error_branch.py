
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from app.main import app
from app.routers import users as users_mod

client = TestClient(app)

def test_router_returns_400_on_integrityerror(monkeypatch):
    def boom(*args, **kwargs):
        raise IntegrityError("dup", params=None, orig=None)
    # Patch the crud used by the router module (ensures lines 15-19,23 execute)
    monkeypatch.setattr(users_mod.crud, "create_user", lambda *a, **k: boom())
    resp = client.post("/api/users", json={"username":"x","email":"x@example.com","password":"p"})
    assert resp.status_code == 400 and "exists" in resp.json()["detail"]
