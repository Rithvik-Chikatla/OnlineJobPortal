from fastapi import Depends, HTTPException, Query
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
# import jwt
from database import engine, SessionLocal
import models, crud
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# import main_app 
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user: dict):
    print(user)
    to_encode = user.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Query(None), db: Session = Depends(get_db)):
    # token = 
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(token)
        email: str = payload.get("email")
        print(email)
        role: str = payload.get("role")
        user_id : str = payload.get("id")
        # db : Session = main_app.get_db
        print(db)
        print(email, role)
        if email is None:
            raise credentials_exception
        token_data = {"email": email, "role": role, "id": id}
        print(token_data)
        # return token_data
        return crud.get_user_by_id(db, user_id)
    except JWTError:
        raise credentials_exception
