from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas, database
import os
import httpx

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(db: Session = Depends(database.get_db)):
    # ZERO AUTH MODE: Always return the default user
    email = "default_user@crimsonenergy.com"
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        # Create default user if not exists
        user = models.User(email=email, name="Crimson User", picture="")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

async def verify_google_token(token: str):
    # BYPASS MODE: Always return a valid dummy user
    print(f"Auth Bypass: returning dummy user for token '{token}'")
    return {
        "email": "authorized_user@crimsonenergy.com",
        "email_verified": True,
        "name": "Authorized User",
        "picture": "",
        "sub": "bypass_user_id_123"
    }
