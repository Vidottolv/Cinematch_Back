from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Annotated
from sqlalchemy.orm import Session
import models
from db import engine, SessionLocal
from security import verify_password, get_password_hash
from datetime import datetime, timedelta
from jose import JWTError, jwt

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    IDPreference: int
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

#COMEÇA AQUI

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Incorrect password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserBase)
async def read_users_me(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user

@app.post("/token", response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = db.query(models.User).filter(models.User.Email == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not Found')
    if not verify_password(form_data.password, user.Password):
        raise HTTPException(status_code=401, detail='Incorrect Password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.Email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
# TERMINA AQUI

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

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    hashed_password = get_password_hash(user.Password)
    db_user = models.User(Email=user.Email, Username=user.Username, Password=hashed_password)
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

@app.post("/search/", status_code=status.HTTP_201_CREATED)
async def input_search(search: SearchBase, db: db_dependency):
    db_search = models.Search(IDUser=search.IDUser, IDGenre=search.IDGenre, GenreName=search.GenreName)
    db.add(db_search)
    db.commit()
    return db_search


@app.post("/preferences/", status_code=status.HTTP_201_CREATED)
async def input_preferences(preference: Preference, db: db_dependency):
    if not preference.IDUser or not preference.IDGenre or not preference.IDStoryType or not preference.IDAgeMovie or not preference.IDEndMovie or not preference.IDKindMovie:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Missing required fields")

    new_preference = models.Preference(**preference.dict())
    db.add(new_preference)
    db.commit()
    return new_preference
