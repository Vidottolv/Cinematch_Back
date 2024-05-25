from fastapi import  FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Annotated
from sqlalchemy.orm import Session
import models
import urllib.parse
from db import engine, SessionLocal
from security import verify_password, get_password_hash


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    Email: EmailStr
    Username: str
    Password: str

class UserLogin(BaseModel):
    Email: EmailStr
    Password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/genres", status_code=status.HTTP_200_OK)
async def get_genres(db: db_dependency):
    genre = db.query(models.Genre).all()
    if genre is None:
        raise HTTPException(status_code=404, detail='Movie was not Found')
    return genre

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    hashed_password = get_password_hash(user.Password)
    db_user = models.User(Email=user.Email, Username=user.Username ,Password=hashed_password)
    db.add(db_user)
    db.commit()
    return db_user

@app.post("/users/{Email}", status_code=status.HTTP_200_OK)
async def login_user(user_login: UserLogin, db: db_dependency):
    user = db.query(models.User).filter(models.User.Email == user_login.Email).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not Found')
    if not verify_password(user_login.Password, user.Password):
        raise HTTPException(status_code=401, detail='Incorrect Password')
    return user
