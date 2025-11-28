
from .. import models, schemas, utils
from fastapi import Depends, FastAPI, HTTPException, Response, status,APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, get_db


router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED,  response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db :Session = Depends(get_db)):

    # lets hash the password
    # hashed_password  = pwd_context.hash(user.password)
    # user.password = hashed_password
    safe_password = user.password[:72]
    hashed_password = utils.hash(safe_password)
    # new_user = models.User(**user.dict())
    new_user = models.User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("PASSWORD LENGTH:", len(user.password))

    return new_user
    
# now we will retrieve information based on a user id
@router.get('/users/{id}', response_model = schemas.UserOut)
def get_user(id: int, db :Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found"
        )
    return user