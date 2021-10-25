# SqlAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# Modulos locales
from . import database

class Dogs(database.Base):
    __tablename__ = 'dogs'
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(20))
    picture = Column(String(200))
    is_adopted = Column(Boolean)
    create_date = Column(DateTime)
    id_user = Column(Integer, ForeignKey('users.id'))


class User(database.Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(40))
    last_name = Column(String(40))
    email = Column(String(60))
    dogs = relationship('Dogs')