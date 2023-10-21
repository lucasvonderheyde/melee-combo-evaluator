from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from database_info import username, password


Base = declarative_base()


class Metadata(Base):
    __tablename__ = 'melee_metadata'

    start_at = Column(String)
    last_frame = Column(Integer) 
    played_on = Column(String)
    game_id = Column(String, primary_key=True)
    
    game_info = relationship("GameInfo", back_populates="metadata_relationship")
    match_info = relationship("MatchInfo", back_populates="metadata_relationship")
    players_info = relationship("PlayersInfo", back_populates="metadata_relationship")
    settings = relationship("Settings", back_populates="metadata_relationship")
    higher_port_player = relationship("HigherPortPlayer", back_populates="metadata_relationship")
    lower_port_player = relationship("LowerPortPlayer", back_populates="metadata_relationship")


class GameInfo(Base):
    __tablename__ = 'game_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_bit_field_1 = Column(Integer)
    game_bit_field_2 = Column(Integer)
    game_bit_field_3 = Column(Integer)
    game_bit_field_4 = Column(Integer)
    bomb_rain_enabled = Column(Boolean)
    item_spawn_behavior = Column(Integer)
    self_destruct_score_value = Column(Integer)
    item_spawn_bit_field_1 = Column(Integer)
    item_spawn_bit_field_2 = Column(Integer)
    item_spawn_bit_field_3 = Column(Integer)
    item_spawn_bit_field_4 = Column(Integer)
    item_spawn_bit_field_5 = Column(Integer)
    damage_ratio = Column(Integer)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="game_info")
    
    

class MatchInfo(Base):
    __tablename__ = 'match_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(String)
    game_number = Column(Integer)
    tiebreaker_number = Column(Integer)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="match_info")


class PlayersInfo(Base):
    __tablename__ = 'players_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_index = Column(Integer)
    port = Column(Integer)
    character_id = Column(Integer)
    type
    start_stocks = Column(Integer)
    character_color = Column(Integer)
    team_shade = Column(Integer)
    handicap = Column(Integer)
    team_id = Column(Integer)
    stamina_mode = Column(Boolean)
    silent_character = Column(Boolean)
    low_gravity = Column(Boolean)
    invisible = Column(Boolean)
    black_stock_icon = Column(Boolean)
    metal = Column(Boolean)
    start_on_angel_platform = Column(Boolean)
    rumble_enabled = Column(Boolean)
    cpu_level = Column(Integer)
    offense_ratio = Column(Integer)
    defense_ratio = Column(Integer)
    model_scale = Column(Integer)
    controller_fix = Column(String)
    name_tag = Column(String)
    display_name = Column(String)
    connect_code = Column(String)
    user_id = Column(String)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    metadata_relationship = relationship("Metadata", back_populates="players_info")
    

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, autoincrement=True)   
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    metadata_relationship = relationship("Metadata", back_populates="settings")

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