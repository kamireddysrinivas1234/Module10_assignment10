
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, security

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, email: str, password: str) -> models.User:
    user = models.User(username=username, email=email, password_hash=security.hash_password(password))
    db.add(user)
    try:
        db.commit()             # success path: commit
    except IntegrityError:       # error path: rollback & re-raise
        db.rollback()
        raise
    db.refresh(user)             # success path: refresh
    return user
