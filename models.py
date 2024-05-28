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

class StoryType(Base):
    __tablename__ = 'TBLStoryType'

    IDStoryType = Column(Integer, primary_key=True, index=True)
    StoryType = Column(String(50))

class AgeMovie(Base):
    __tablename__ = 'TBLAgeMovie'

    IDAgeMovie = Column(Integer, primary_key=True, index=True)
    AgeMovie = Column(String(50))

class EndMovie(Base):
    __tablename__ = 'TBLEndMovie'

    IDEndMovie = Column(Integer, primary_key=True, index=True)
    EndMovie = Column(String(50))

class KindMovie(Base):
    __tablename__ = 'TBLKindMovie'

    IDKindMovie = Column(Integer, primary_key=True, index=True)
    KindMovie = Column(String(50))