from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class Group_(Base):
    __tablename__ = 'Group_'
    id = Column(Integer,primary_key=True)
    name = Column(String(80),unique=True)
    email = Column(String(80),unique=True)
    size = Column(Integer, default=5, nullable=False)

    def __repr__(self):
        return "<Group_(name='%s', id='%s',email='%s',size='%s')>" % (self.name,self.id,self.email,self.size)

    @classmethod
    def get_id(cls, session, id):
        return session.query(Group_).filter(Group_.id == id).one()

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(Group_).filter(Group_.name == name).one()

   

    FIELDS = {
        'id': int,
        'name': str,
        'email': str,
        'size': int,
    }

    FIELDS.update(Base.FIELDS)