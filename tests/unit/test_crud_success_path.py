
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base
from app import crud

def test_create_user_success_commit_and_refresh():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = Session()
    user = crud.create_user(db, "alice", "alice@example.com", "pw")
    assert user.id is not None and user.username == "alice"
    # getters to cover lines before create_user
    assert crud.get_user_by_username(db, "alice").email == "alice@example.com"
    assert crud.get_user_by_email(db, "alice@example.com").username == "alice"
    db.close()
