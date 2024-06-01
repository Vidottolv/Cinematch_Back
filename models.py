from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
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

class Preferences(Base):
    __tablename__ = 'TBLPreferences'

    IDPreference = Column(Integer, primary_key=True, index=True)
    IDUser = Column(Integer, ForeignKey('TBLUsers.IDUser'))
    IDGenre = Column(Integer, ForeignKey('TBLGenres.IDGenre'))
    GenreName = relationship("Genre", backref="preferences")
    IDStoryType = Column(Integer, ForeignKey('TBLStoryType.IDStoryType'))
    StoryType = relationship("StoryType", backref="preferences")
    IDAgeMovie = Column(Integer, ForeignKey('TBLAgeMovie.IDAgeMovie'))
    AgeMovie = relationship("AgeMovie", backref="preferences")
    IDEndMovie = Column(Integer, ForeignKey('TBLEndMovie.IDEndMovie'))
    EndMovie = relationship("EndMovie", backref="preferences")
    IDKindMovie = Column(Integer, ForeignKey('TBLKindMovie.IDKindMovie'))
    KindMovie = relationship("KindMovie", backref="preferences")

class Search(Base):
    __tablename__ = 'TBLSearchEv'

    IDSearch = Column(Integer, primary_key=True, index=True)
    IDUser = Column(Integer, ForeignKey('TBLUsers.IDUser'))
    IDGenre = Column(Integer, ForeignKey('TBLGenres.IDGenre'))
    GenreName = relationship("Genre", backref="preferences")