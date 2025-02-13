from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas, database, models, oauth2, utils
from database import get_db
router = APIRouter(prefix = "/auth",
                   tags= ["Login"])

@router.post("/login", response_model=schemas.UserToken)
async def login(user_credential:schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username==user_credential.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid username and password..")
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid username and password..")
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    return {"access_token": access_token, "token_type":"bearer"}

