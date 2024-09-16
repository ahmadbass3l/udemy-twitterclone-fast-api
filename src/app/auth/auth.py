import datetime
import os

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.db_and_models.models import User
from app.db_and_models.session import get_session

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_IN_MINUTE = os.environ.get("ACCESS_TOKEN_EXPIRE_IN_MINUTE")


pwd_context = CryptContext(schemes=["bcrypt"])
oatuh2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plane_pwd, hashed_pw):
    return pwd_context.verify(secret=plane_pwd, hash=hashed_pw)


def create_access_token(user: User):
    try:
        claims = {
            "sub": user.username,
            "email": user.email,
            "exp": datetime.datetime.now()
            + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTE),
        }
        return jwt.encode(claims=claims, key=SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise JWTError("Wrong token decoding")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise JWTError("Can'T decode token")


async def get_current_user(
    token: str = Depends(oatuh2_scheme), db: Session = Depends(get_session)
):
    payload = verify_token(token)
    user_name = payload.get("sub")
    user = db.exec(select(User).where(User.username == user_name)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not Found!")
    return user
