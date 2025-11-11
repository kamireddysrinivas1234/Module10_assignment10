
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db import Base, get_db

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

def test_duplicate_user_hits_except_and_400_and_list():
    r1 = client.post("/api/users", json={"username":"u1","email":"u1@example.com","password":"p"})
    assert r1.status_code == 201
    r2 = client.post("/api/users", json={"username":"u1","email":"u1@example.com","password":"p"})
    assert r2.status_code == 400 and "exists" in r2.json()["detail"]
    r3 = client.get("/api/users")
    assert r3.status_code == 200 and any(u["username"]=="u1" for u in r3.json())
