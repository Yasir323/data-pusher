import os

from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get("DB_URI")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    website = Column(String, nullable=True)
    destinations = relationship("Destination", back_populates="account", cascade="all, delete-orphan")


class Destination(Base):
    __tablename__ = 'destinations'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    http_method = Column(String, nullable=False)
    headers = Column(JSON, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="destinations")
