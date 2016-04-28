import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.types import DateTime
from datetime import datetime
from urlparse import urljoin
from flask import request


def make_external(url):
    return urljoin(request.url_root, url)


Base = declarative_base()


class Shares(Base):
    __tablename__ = 'shares'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    rem_host = Column(String(80), nullable=False)
    address = Column(String(80), nullable=False)
    worker = Column(String(80), nullable=False)
    our_result = Column(String(250), nullable=False)
    upstream_result = Column(String(250), nullable=False)
    difficulty = Column(String(80), nullable=False)
    reason = Column(String(80))
    solution = Column(String(250), nullable=False)


class Blocks(Base):
    __tablename__ = 'blocks'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    height = Column(String(80), nullable=False)
    blockhash = Column(String(250), nullable=False)
    confirmations = Column(String(80), nullable=False)
    accounted = Column(String(80), nullable=False)


class Miners(Base):
    __tablename__ = 'miners'
    id = Column(Integer, primary_key=True)
    address = Column(String(80), nullable=False)
    worker = Column(String(80), nullable=False)
    hashrate = Column(String(80), nullable=False)
    difficulty = Column(String(80), nullable=False)


engine = create_engine('mysql://pool_user:Sp3ctrum@localhost/methpool')

Base.metadata.create_all(engine,  checkfirst=True)
