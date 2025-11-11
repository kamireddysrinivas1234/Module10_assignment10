
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
from app.main import app
from app.db import Base, get_db
from app import security
from app.routers import users as users_mod

# Use shared in-memory DB
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_router_success_create_and_list_with_stubbed_hash(monkeypatch):
    monkeypatch.setattr(security, "hash_password", lambda _: "H")
    r = client.post("/api/users", json={"username":"ok","email":"ok@example.com","password":"secret1"})
    assert r.status_code == 201, r.text
    r2 = client.get("/api/users")
    assert r2.status_code == 200 and any(u["username"]=="ok" for u in r2.json())

def test_router_integrity_error_400(monkeypatch):
    # Make sure hash won't error
    monkeypatch.setattr(security, "hash_password", lambda _: "H")
    # Force crud to raise IntegrityError to cover except path
    def boom(*args, **kwargs): raise IntegrityError("dup", params=None, orig=None)
    monkeypatch.setattr(users_mod.crud, "create_user", boom)
    r = client.post("/api/users", json={"username":"dup","email":"dup@example.com","password":"secret1"})
    assert r.status_code == 400 and "exists" in r.json()["detail"]
