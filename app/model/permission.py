from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class Permission(Base):
    __tablename__ = 'Permission'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)

    def __repr__(self):
        return "<Permission(name='%s')>" % (self.name)

    @classmethod
    def get_id(cls, session, id):
        return session.query(Permission).filter(Permission.id == id).one()

    @classmethod
    def find_by_name(cls, session, name):
        try:
            result = session.query(Permission).filter(Permission.name == name).one()
        except NoResultFound:
            result = None
        return result

    FIELDS = {
        'name': str
    }

    FIELDS.update(Base.FIELDS)