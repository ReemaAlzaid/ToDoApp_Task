from schemas.user import CreateUser
from models.user import User
import libs.auth
from database import Base, engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

Base.metadata.create_all(engine)
app=FastAPI()
app.include_router(libs.auth.router)