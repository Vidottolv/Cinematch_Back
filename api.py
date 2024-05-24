from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from db import engine, SessionLocal
from security import verify_password, get_password_hash

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class MovieBase(BaseModel):
    Title: str
    Content: str

class UserBase(BaseModel):
    Email: str
    Password: str

class UserLogin(BaseModel):
    Email: str
    Password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/movies/", status_code=status.HTTP_201_CREATED)
async def create_movie(movie: MovieBase, db: db_dependency):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    return db_movie

@app.get("/movies/{id_movie}", status_code=status.HTTP_200_OK)
async def read_movie(id_movie: int, db: db_dependency):
    movie = db.query(models.Movie).filter(models.Movie.IdMovie == id_movie).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie was not Found')
    return movie

@app.delete("/movies/{id_movie}", status_code=status.HTTP_200_OK)
async def delete_movie(id_movie: int, db: db_dependency):
    movie = db.query(models.Movie).filter(models.Movie.IdMovie == id_movie).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie was not Found')
    db.delete(movie)
    db.commit()
    return {"detail": "Movie deleted successfully"}

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    hashed_password = get_password_hash(user.Password)
    db_user = models.User(Email=user.Email, Password=hashed_password)
    db.add(db_user)
    db.commit()
    return db_user

@app.get("/users/{Email}", status_code=status.HTTP_200_OK)
async def login_user(user_login: UserLogin, db: db_dependency):
    user = db.query(models.User).filter(models.User.Email == user_login.Email).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not Found')
    if not verify_password(user_login.Password, user.Password):
        raise HTTPException(status_code=401, detail='Incorrect Password')
    return user
