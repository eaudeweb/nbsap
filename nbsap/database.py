from flaskext.openid import OpenID
from flask.ext.pymongo import PyMongo
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

oid = OpenID()
mongo = PyMongo()

DATABASE_URI = 'sqlite:////tmp/flask-openid.db'

engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    openid = Column(String(200))

    def __init__(self, openid):
        self.openid = openid

