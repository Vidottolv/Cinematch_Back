from sqlalchemy import Boolean, Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = 'TBLUsers'

    IDUser = Column(Integer, primary_key=True, index=True)
    Username = Column(String(50), unique=True)
    

class Movie(Base):
    __tablename__ = 'TBLMovies'

    IdMovie = Column(Integer, primary_key=True, index=True)
    Title = Column(String(50))
    Content = Column(String(100))

