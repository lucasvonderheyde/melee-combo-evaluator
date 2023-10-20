from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from database_info import username, password


Base = declarative_base()


class Metadata(Base):
    __tablename__ = 'melee_metadata'

    game_id = Column(String, primary_key=True)
    lastFrame = Column(Integer)

    game_info = relationship("GameInfo", back_populates="metadata")
    match_info = relationship("MatchInfo", back_populates="metadata")
    players_info = relationship("PlayersInfo", back_populates="metadata")
    settings = relationship("Settings", back_populates="metadata")
    higher_port_player = relationship("HigherPortPlayer", back_populates="metadata")
    lower_port_player = relationship("LowerPortPlayer", back_populates="metadata")


class GameInfo(Base):
    __tablename__ = 'game_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    metadata_relationship = relationship("Metadata", back_populates="game_info")

class MatchInfo(Base):
    __tablename__ = 'match_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    metadata_relationship = relationship("Metadata", back_populates="game_info")

class PlayersInfo(Base):
    __tablename__ = 'players_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    metadata_relationship = relationship("Metadata", back_populates="game_info")

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, autoincrement=True)   
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    metadata_relationship = relationship("Metadata", back_populates="game_info")

class HigherPortPlayer(Base):
    __tablename__ = "higher_port_player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    frame = Column(Integer)
    metadata_relationship = relationship("Metadata", back_populates="higher_port_player")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='uix_1'),)

class LowerPortPlayer(Base):
    __tablename__ = "lower_port_player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    frame = Column(Integer)
    metadata_relationship = relationship("Metadata", back_populates="lower_port_player")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='uix_2'),)



engine = create_engine(f'postgresql://{username}:{password}@localhost/Melee_Combo_Database')

Base.metadata.create_all(engine)