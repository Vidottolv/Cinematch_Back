from fastapi import FastAPI, HTTPException, Depends, Query, status
from pydantic import BaseModel, EmailStr
from typing import Annotated
from sqlalchemy.orm import Session
import models
from db import engine, SessionLocal
from security import verify_password, get_password_hash

SECRET_KEY = "b10f469883d28ac3ef86cc14c5e0ed21148c507ea9635ea3da0ce95a245c2608"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

class UserBase(BaseModel):
    Email: EmailStr
    Username: str
    Password: str

class UserLogin(BaseModel):
    Email: EmailStr
    Password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class Preference(BaseModel):
    IDUser: int
    IDGenre: int
    GenreName: str
    IDStoryType: int
    StoryType: str
    IDAgeMovie: int
    AgeMovie: str
    IDEndMovie: int
    EndMovie: str
    IDKindMovie: int
    KindMovie: str

class SearchBase(BaseModel):
    IDSearch: int
    IDUser: int
    IDGenre: int
    GenreName: str

class SearchPost(BaseModel):
    IDUser: int
    IDGenre: int
    GenreName: str

class ChooseBase(BaseModel):
    IDChoose: int
    IDUser: int
    IDGenre: int
    GenreName: str

class ChoosePost(BaseModel):
    IDUser: int
    IDGenre: int
    GenreName: str
    MovieName: str


@app.get("/genres", status_code=status.HTTP_200_OK)
async def get_genres(db: db_dependency):
    genre = db.query(models.Genre).all()
    if genre is None:
        raise HTTPException(status_code=404, detail='Genre was not Found')
    return genre

@app.get("/storytype", status_code=status.HTTP_200_OK)
async def get_storytypes(db: db_dependency):
    storytype = db.query(models.StoryType).all()
    if storytype is None:
        raise HTTPException(status_code=404, detail='StoryType was not Found')
    return storytype

@app.get("/agemovie", status_code=status.HTTP_200_OK)
async def get_agemovies(db: db_dependency):
    agemovie = db.query(models.AgeMovie).all()
    if agemovie is None:
        raise HTTPException(status_code=404, detail='AgeMovie was not Found')
    return agemovie

@app.get("/endmovie", status_code=status.HTTP_200_OK)
async def get_endmovies(db: db_dependency):
    endmovie = db.query(models.EndMovie).all()
    if endmovie is None:
        raise HTTPException(status_code=404, detail='EndMovie was not Found')
    return endmovie

@app.get("/kindmovie", status_code=status.HTTP_200_OK)
async def get_kindmovies(db: db_dependency):
    kindmovie = db.query(models.KindMovie).all()
    if kindmovie is None:
        raise HTTPException(status_code=404, detail='KindMovie was not Found')
    return kindmovie

@app.post("/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    hashed_password = get_password_hash(user.Password)
    db_user = models.User(Email=user.Email, Username=user.Username, Password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login_user/{Email}", status_code=status.HTTP_200_OK)
async def login_user(user_login: UserLogin, db: db_dependency):
    user = db.query(models.User).where(models.User.Email == user_login.Email).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not Found')
    if not verify_password(user_login.Password, user.Password):
        raise HTTPException(status_code=401, detail='Incorrect Password')
    return user

@app.post("/search/", status_code=status.HTTP_201_CREATED)
async def input_search(search: SearchPost, db: db_dependency):
    db_search = models.Search(IDUser=search.IDUser, \
                              IDGenre=search.IDGenre, \
                              GenreName=search.GenreName)
    db.add(db_search)
    db.commit()
    return db_search

@app.post("/choose/", status_code=status.HTTP_201_CREATED)
async def input_choose(choose: ChoosePost, db: db_dependency):
    db_choose = models.Choose(IDUser=choose.IDUser, \
                              IDGenre=choose.IDGenre, \
                              GenreName=choose.GenreName, \
                              MovieName=choose.MovieName)
    db.add(db_choose)
    db.commit()
    return db_choose

@app.get("/most_choosed", status_code=status.HTTP_200_OK)
async def get_most_choosed(db: db_dependency, IDUser: int = Query(...)):
    choosed = db.query(models.Choose).where(models.Choose.IDUser == IDUser).all()
    genre_counts = {}
    for choice in choosed:
        genre_counts[choice.GenreName] = genre_counts.get(choice.GenreName, 0) + 1
    most_viewed_genre = max(genre_counts, key=genre_counts.get)
    return most_viewed_genre

@app.post("/preferences/", status_code=status.HTTP_201_CREATED)
async def input_preferences(preference: Preference, db: db_dependency):
    new_preference = models.Preferences(IDUser=preference.IDUser, \
                                        IDGenre=preference.IDGenre, GenreName=preference.GenreName, \
                                        IDStoryType=preference.IDStoryType, StoryType=preference.StoryType, \
                                        IDAgeMovie=preference.IDAgeMovie, AgeMovie=preference.AgeMovie, \
                                        IDEndMovie=preference.IDEndMovie, EndMovie=preference.EndMovie, \
                                        IDKindMovie=preference.IDKindMovie, KindMovie=preference.KindMovie)
    db.add(new_preference)
    db.commit()
    return new_preference
