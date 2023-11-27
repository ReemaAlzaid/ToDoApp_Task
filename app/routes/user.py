from datetime import timedelta
from fastapi import Depends, HTTPException, status , APIRouter
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from starlette import status
from passlib.context import CryptContext
from services.auth import authenticate_user,createToken
from database import db_dependency
from models.user import User
from models.todolist import ToDoList
from schemas.user import CreateUser,Token
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

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def createUser(db:db_dependency,UserReq: CreateUser):
    new_user = User(email=UserReq.email,password=pwd_context.hash(UserReq.password))
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        new_list = ToDoList(owner_id=new_user.id)
        db.add(new_list)
        db.commit()
        return 
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
    token = createToken(user.email,user.id,timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))

    return {"access_token": token, "token_type": "bearer"}