from dotenv import load_dotenv, find_dotenv
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
load_dotenv(find_dotenv())
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentails_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentails_exception
        token_data = TokenData(id=id, token=token)
    except JWTError:
        raise credentails_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentails_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
        "message": "user id not found"}, headers={'WWW-Authenicate': 'Bearer'})

    return verify_token(token, credentails_exception)
