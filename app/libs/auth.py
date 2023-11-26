from datetime import datetime, timedelta
from imaplib import _Authenticator
from fastapi import Depends, HTTPException, status , APIRouter
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import SessionLocal
from models.user import User
from schemas.user import CreateUser,Token
from typing import Annotated

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2: OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def createUser(db:db_dependency,UserReq: CreateUser):
    new_user = User(email=UserReq.email,password=pwd_context.hash(UserReq.password))
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        raise HTTPException(status_code=409, detail="This email is already registered")
    
@router.post("/login", response_model=Token)
async def login_for_access_token(db:db_dependency,form_data: Annotated[OAuth2PasswordRequestForm ,Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = createToken(user.email,user.id,timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(db:db_dependency,email:str, password:str):
    print(email)
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
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)