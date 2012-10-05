from flaskext.openid import OpenID
from flask.ext.pymongo import PyMongo
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

oid = OpenID()
mongo = PyMongo()

session_factory = sessionmaker()
db_session = scoped_session(session_factory)

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    openid = Column(String(200))

    def __init__(self, openid):
        self.openid = openid

