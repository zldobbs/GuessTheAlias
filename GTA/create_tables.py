import os
import sys
from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, \
    Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Rooms(Base):
    __tablename__ = 'Rooms'

    roomID = Column(String(6), primary_key=True)
    roomState = Column(String(8), nullable=True)
    currentAlias_FK = Column(Integer, ForeignKey("Players.userID"))
    roomCreator_FK = Column(Integer, ForeignKey("Players.userID"))

    alias = relationship("alias", foreign_keys="Rooms.currentAlias_FK")
    creator = relationship("creator", foreign_keys="Rooms.roomCreator_FK")

class Teams(Base):
    __tablename__ = 'Teams'

    # Str len is 13: 
        # color name len = max(6)
        # concat 2 colors = max(6) + '-' + max(6)
        # total str len = 13
    color = Column(String(13), primary_key=True) 
    rooms_FK = Column(String(6), primary_key=True)
    Score = Column(Integer)

    room = relationship("room", foreign_keys="Rooms.roomID")
 
class Players(Base):
    __tablename__ = 'Players'

    userID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    hint1 = Column(Text, nullable=True)
    hint2 = Column(Text, nullable=True)
    hint3 = Column(Text, nullable=True)
    hint4 = Column(Text, nullable=True)
    hint5 = Column(Text, nullable=True)
    hint6 = Column(Text, nullable=True)
    color_FK = Column(String(13))
    rooms_FK = Column(String(6))

    __table_args__ = (ForeignKeyConstraint([color_FK, rooms_FK],
                                           [Teams.color, Teams.rooms_FK]),
                      {})

# SQL
    # Username = root
    # password = password

engine = create_engine('mysql:///sqlalchemy_example.db')
# engine = create_engine('mysql://tiger:hentai@e34.204.52.88') # connect to server
engine.execute("CREATE DATABASE IF NOT EXISTS gta") #create db
engine.execute("USE gta") # select db

# Create all tables in the engine
Base.metadata.create_all(engine)