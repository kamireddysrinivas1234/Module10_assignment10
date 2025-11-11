
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..db import get_db, Base, engine
from .. import schemas, crud, models

# Ensure tables exist for whichever DB engine is active
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("", response_model=schemas.UserRead, status_code=201)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db, payload.username, payload.email, payload.password)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return user

@router.get("", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).order_by(models.User.id.asc()).all()
