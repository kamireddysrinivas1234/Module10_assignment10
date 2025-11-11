
from sqlalchemy.exc import IntegrityError
from app import crud

class DummySession:
    def __init__(self): self.added = []; self.rollback_called = False
    # Methods used by create_user
    def add(self, obj): self.added.append(obj)
    def commit(self): raise IntegrityError('dup', params=None, orig=None)
    def rollback(self): self.rollback_called = True
    def refresh(self, obj): pass  # not reached on error

def test_create_user_integrity_error_triggers_rollback():
    db = DummySession()
    try:
        crud.create_user(db, "u", "u@example.com", "pw")
        assert False, "expected IntegrityError"
    except IntegrityError:
        # ensure rollback branch ran inside create_user
        assert db.rollback_called is True
