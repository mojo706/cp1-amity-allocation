""" Contains the DB schema for the amity cli app"""

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class PersonModel(Base):
    """create a person table"""
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    office_space = Column(String(32), ForeignKey('room.name'))
    living_space = Column(String(32), ForeignKey('room.name'))

class RoomModel(Base):
    """Create the rooms table
    """
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    room_type = Column(String(32), nullable=False)
    room_capacity = Column(Integer, nullable=False)
    room_occupants = relationship("PersonModel", foreign_keys="PersonModel.office_space")
    room_occupants = relationship("PersonModel", foreign_keys="PersonModel.living_space")

class CreateDb(object):
    """creating database connection to object"""

    def __init__(self, db_name=None):
        self.db_name = db_name
        if self.db_name:
            self.db_name = db_name + '.db'
        else:
            self.db_name = 'main.db'
        self.engine = create_engine('sqlite:///' + self.db_name)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)