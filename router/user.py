from fastapi import APIRouter, Depends, status, HTTPException
import schemas, models, oauth2, utils
from sqlalchemy.orm import Session 
from database import get_db
from typing import List

router = APIRouter(prefix="/adminpanel", tags=["Users"])

@router.post("/createuser",status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def createUser(user:schemas.UserCreate, db:Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def getUser(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"User detail not found !!")
    return user

@router.get("/users/all", response_model=List[schemas.UserOut])
def getallUser(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User detail not found !!")
    return users
