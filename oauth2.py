from fastapi import HTTPException, Depends, status
from jose import JWTError
import jwt
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database, schemas, models,oauth2
from database import get_db

oauth2.schemes = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = '330834a238bc0db378fc3484b41495b213c21b35d99b2a9800545566fbd3634f'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expiry_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        id: str= payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data= schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str=Depends(oauth2.schemes), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                          detail = f"could not validate credentials",
                                          headers = {"WWW-BEARER"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user