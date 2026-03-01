from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    username=Column(String)
    password = Column(String)
    role = Column(String,default="user")


class Book(Base):
    __tablename__ = "books"

    id=Column(Integer,primary_key=True)
    title=Column(String)
    author = Column(String,default="Unknown")
    price = Column(Integer)