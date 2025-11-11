
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
from app.db import Base
from app.schemas import UserCreate
from app.routers import users as users_mod

def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)()

def test_router_create_user_integrityerror_results_in_http_400(monkeypatch):
    db = make_session()
    # Monkeypatch crud used inside the router to raise IntegrityError
    def boom(*args, **kwargs): raise IntegrityError("dup", params=None, orig=None)
    monkeypatch.setattr(users_mod.crud, "create_user", boom)
    with pytest.raises(Exception) as exc:
        users_mod.create_user(UserCreate(username="abc", email="a@b.com", password="secret1"), db)
    assert "400" in str(exc.value) or "exists" in str(exc.value)
    db.close()
