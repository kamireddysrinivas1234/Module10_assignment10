
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
from app.db import Base
from app import crud

def test_getters_cover_lines_7_and_10_and_success_branch():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = Session()
    u = crud.create_user(db, "alice", "alice@example.com", "pw")
    # explicitly exercise both getters (crud.py lines 7 and 10)
    assert crud.get_user_by_email(db, "alice@example.com").username == "alice"
    assert crud.get_user_by_username(db, "alice").email == "alice@example.com"
    db.close()

class DummySession:
    def __init__(self): self.rollback_called = False
    def add(self, obj): pass
    def commit(self): raise IntegrityError("dup", params=None, orig=None)
    def rollback(self): self.rollback_called = True
    def refresh(self, obj): pass

def test_create_user_integrityerror_triggers_rollback_lines_14_21():
    db = DummySession()
    with pytest.raises(IntegrityError):
        crud.create_user(db, "x", "x@example.com", "pw")
    assert db.rollback_called is True
