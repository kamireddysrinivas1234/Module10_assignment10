
import pytest
from sqlalchemy.exc import IntegrityError
from app.routers import users as users_mod
from app.schemas import UserCreate

class DummyDB: pass

def test_router_create_user_except_branch_lines_15_19_23(monkeypatch):
    # Force crud.create_user used inside router to raise IntegrityError
    def boom(db, username, email, password):
        raise IntegrityError("dup", params=None, orig=None)
    monkeypatch.setattr(users_mod.crud, "create_user", boom)
    payload = UserCreate(username="u", email="u@example.com", password="pw")
    with pytest.raises(Exception) as exc:
        users_mod.create_user(payload, DummyDB())  # call function directly
    # FastAPI raises HTTPException (status_code=400) from router
    assert "400" in str(exc.value) or "exists" in str(exc.value)
