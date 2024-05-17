from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class MovieBase(BaseModel):
    Title: str
    Content: str

class userBase(BaseModel):
    Username: set

def get_db():
    datab = SessionLocal()
    try:
        yield datab
    finally:
        datab.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/movies/", status_code=status.HTTP_201_CREATED)
async def create_movie(movie: MovieBase, db: db_dependency):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()

@app.get("/movies/{IDMovie}", status_code=status.HTTP_200_OK)
async def read_movie (id_movie: int, db: db_dependency):
    movie = db.query(models.Movie).filter(models.Movie.IdMovie == id_movie).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie was not Found')
    return movie

@app.delete("/movies/{IDMovie}", status_code=status.HTTP_200_OK)
async def delete_movie(id_movie: int, db: db_dependency):
    movie = db.query(models.Movie).filter(models.Movie.IdMovie == id_movie).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie was not Found')
    db.delete(movie)
    db.commit()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: userBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.IDUser == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not Found')
    return user