from sqlalchemy import Boolean, Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = 'TBLUsers'

    IDUser = Column(Integer, primary_key=True, index=True)
    Email = Column(String(50), unique=True)
    Username = Column(String(50))
    Password = Column(String(200))
    

class Genre(Base):
    __tablename__ = 'TBLGenres'

    IDGenre = Column(Integer, primary_key=True, index=True)
    GenreName = Column(String(50))

