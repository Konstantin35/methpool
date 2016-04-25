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
    username = Column(String(80), nullable=False)
    our_result = Column(String(250), nullable=False)
    upstream_result = Column(String(250), nullable=False)
    difficulty = Column(String(80), nullable=False)
    reason = Column(String(80), nullable=False)
    solution = Column(String(250), nullable=False)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    social_id = Column(String(64), nullable=False, unique=True)


class SaleItem(Base):
    __tablename__ = 'sale_item'
    __searchable__ = ['description']
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    image_name = Column(String(250))
    category_name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_name = Column(String(250), nullable=False)
    contact = Column(String(250))
    last_updated = Column(DateTime, nullable=False)
    user = relationship(Users)

    def __init__(self, name, description, price, image_name, category_name, user_id, user_name, contact,
                 last_updated=None):
        self.name = name
        self.description = description
        self.price = price
        self.image_name = image_name
        self.category_name = category_name
        self.user_id = user_id
        self.user_name = user_name
        self.contact = contact
        self.last_updated = datetime.utcnow()

    def __repr__(self):
        return '<sale_item %d>' % self.id

        # We added this serialize function to be able to send JSON objects in a serializable format

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category_name': self.category_name,
            'user_name': self.user_name,
            'contact': self.contact,
            'url': make_external('/forsale/%s/single_item' % self.id)
        }


engine = create_engine('mysql://pool_user:Sp3ctrum@localhost/methpool')

Base.metadata.create_all(engine)
