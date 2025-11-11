
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base
from app.schemas import UserCreate
from app.routers import users as users_mod

def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    # Create tables on THIS engine before using the session
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)()

def test_router_direct_success_and_list_hits_returns():
    db = make_session()
    payload = UserCreate(username="validuser", email="valid@example.com", password="secret1")
    user = users_mod.create_user(payload, db)   # should return the created user (line 19)
    assert user.username == "validuser"
    items = users_mod.list_users(db)            # should return list (line 23)
    assert any(u.username == "validuser" for u in items)
    db.close()
