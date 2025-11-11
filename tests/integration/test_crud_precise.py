
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
from app.db import Base
from app import crud

def _session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)()

def test_crud_success_and_getters_cover_all():
    db = _session()
    u = crud.create_user(db, "alice", "alice@example.com", "pw")
    assert crud.get_user_by_username(db, "alice").email == "alice@example.com"
    assert crud.get_user_by_email(db, "alice@example.com").username == "alice"
    db.close()

def test_crud_duplicate_triggers_integrityerror_and_rollback():
    db = _session()
    crud.create_user(db, "dup", "dup@example.com", "p1")
    with pytest.raises(IntegrityError):
        crud.create_user(db, "dup", "dup@example.com", "p2")
    db.close()
