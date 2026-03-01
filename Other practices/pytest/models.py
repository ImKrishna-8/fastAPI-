from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True)
    username = Column(String,nullable=False)
    password = Column(String,nullable=False)
    role = Column(String,default='user')

class Game(Base):
    __tablename__ = "games"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    size=Column(Integer)
