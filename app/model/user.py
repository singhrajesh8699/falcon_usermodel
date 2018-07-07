# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy

user_permission = Table('user_permission',Base.metadata,
	Column('permission_id', Integer, ForeignKey('Permission.id',ondelete='cascade'),primary_key=True),
	Column('user_id', Integer, ForeignKey('User.id',ondelete='cascade'),primary_key=True)
)

user_group = Table('user_group',Base.metadata,
	Column('group_id', Integer, ForeignKey('Group_.id',ondelete='cascade'),primary_key=True),
	Column('user_id', Integer, ForeignKey('User.id',ondelete='cascade'),primary_key=True)
)

user_owner = Table('user_owner',Base.metadata,
    Column('owner_id', Integer, ForeignKey('Owner.id',ondelete='cascade'),primary_key=True),
	Column('user_id', Integer, ForeignKey('User.id',ondelete='cascade'),primary_key=True)
)

class User(Base):

    __tablename__ = 'User'
    id = Column(Integer,primary_key=True)
    username = Column(String(80),unique=True)
    password = Column(String(200))
    email = Column(String(256),unique=True)
    phone = Column(String(80))
    is_active = Column(Integer,default=0)
    
    ownership = relationship('Owner', secondary=user_owner, \
	lazy='dynamic', backref=backref('User', lazy='dynamic'))
    
    permissions = relationship('Permission', secondary=user_permission,  \
	lazy='dynamic', backref=backref('User', lazy='dynamic'))

    groups = relationship('Group_', secondary=user_group, \
	lazy='dynamic', backref=backref('User', lazy='dynamic'))

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" % \
            (self.id,self.username, self.email)

    @classmethod
    def get_id(cls, session, id_):
        return session.query(User).filter(User.id == id_).one()

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(User).filter(User.email == email).one()

    FIELDS = {
        'id' : int,
        'username': str,
        'email': str,
        'password': str,
        'phone': str
    }

    FIELDS.update(Base.FIELDS)



class Owner(Base):
    __tablename__ = 'Owner'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer,default=0)

    def __repr__(self):
        return "<Owner(owner_id='%s')>" % (self.owner_id)

    @classmethod
    def get_id(cls, session, owner_id):
        try:
            result = session.query(Owner).filter(Owner.owner_id == owner_id).one()
        except NoResultFound:
            result = None
        return result

    FIELDS = {
        'owner_id': int
    }

    FIELDS.update(Base.FIELDS)

