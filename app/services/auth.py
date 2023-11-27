from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status , APIRouter
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from starlette import status
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import SessionLocal,db_dependency
from models.user import User
from typing import Annotated
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")


def authenticate_user(db:db_dependency,email:str, password:str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password,user.password):
        return False
    return user

def createToken(email:str,userId:int,deltaExpire:timedelta):
    encode = {'sub': email, 'id':userId}
    expires = datetime.utcnow()+deltaExpire
    encode.update({'exp':expires})
    return jwt.encode(encode,os.getenv("SECRET_KEY"),algorithm=os.getenv("ALGORITHM"))

async def validateUser(token: Annotated[str,Depends(oauth2)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        print(token)
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception