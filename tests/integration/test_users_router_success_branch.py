
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db import Base, get_db

# Wire an in-memory DB into the app so we can create a real user too
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

def test_router_success_create_and_list():
    r = client.post("/api/users", json={"username":"ok","email":"ok@example.com","password":"pw"})
    assert r.status_code == 201
    r2 = client.get("/api/users")
    assert r2.status_code == 200 and any(u["username"] == "ok" for u in r2.json())
