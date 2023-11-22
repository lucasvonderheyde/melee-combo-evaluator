from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean, UniqueConstraint, BigInteger, Double
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from database_info import database
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class Metadata(Base):
    __tablename__ = 'melee_metadata'

    start_at = Column(String)
    last_frame = Column(BigInteger) 
    played_on = Column(String)
    game_id = Column(String, primary_key=True)
    
    game_info = relationship("GameInfo", back_populates="metadata_relationship")
    match_info = relationship("MatchInfo", back_populates="metadata_relationship")
    players_info = relationship("PlayersInfo", back_populates="metadata_relationship")
    settings = relationship("Settings", back_populates="metadata_relationship")
    higher_port_player_post_frames = relationship("HigherPortPlayerPostFrames", back_populates="metadata_relationship")
    lower_port_player_post_frames = relationship("LowerPortPlayerPostFrames", back_populates="metadata_relationship")
    higher_port_player_pre_frames = relationship("HigherPortPlayerPreFrames", back_populates="metadata_relationship")
    lower_port_player_pre_frames = relationship("LowerPortPlayerPreFrames", back_populates="metadata_relationship")
    user_id = Column(Integer, ForeignKey('users.id'))

class GameInfo(Base):
    __tablename__ = 'game_info'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    game_bit_field_1 = Column(BigInteger)
    game_bit_field_2 = Column(BigInteger)
    game_bit_field_3 = Column(BigInteger)
    game_bit_field_4 = Column(BigInteger)
    bomb_rain_enabled = Column(Boolean)
    item_spawn_behavior = Column(BigInteger)
    self_destruct_score_value = Column(BigInteger)
    item_spawn_bit_field_1 = Column(BigInteger)
    item_spawn_bit_field_2 = Column(BigInteger)
    item_spawn_bit_field_3 = Column(BigInteger)
    item_spawn_bit_field_4 = Column(BigInteger)
    item_spawn_bit_field_5 = Column(BigInteger)
    damage_ratio = Column(BigInteger)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="game_info")
    
    

class MatchInfo(Base):
    __tablename__ = 'match_info'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    match_id = Column(String)
    game_number = Column(BigInteger)
    tiebreaker_number = Column(BigInteger)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="match_info")


class PlayersInfo(Base):
    __tablename__ = 'players_info'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    player_index = Column(BigInteger)
    port = Column(BigInteger)
    character_id = Column(BigInteger)
    player_type = Column(BigInteger)
    start_stocks = Column(BigInteger)
    character_color = Column(BigInteger)
    team_shade = Column(BigInteger)
    handicap = Column(BigInteger)
    team_id = Column(BigInteger)
    stamina_mode = Column(Boolean)
    silent_character = Column(Boolean)
    low_gravity = Column(Boolean)
    invisible = Column(Boolean)
    black_stock_icon = Column(Boolean)
    metal = Column(Boolean)
    start_on_angel_platform = Column(Boolean)
    rumble_enabled = Column(Boolean)
    cpu_level = Column(BigInteger)
    offense_ratio = Column(BigInteger)
    defense_ratio = Column(BigInteger)
    model_scale = Column(BigInteger)
    controller_fix = Column(String)
    name_tag = Column(String)
    display_name = Column(String)
    connect_code = Column(String)
    user_id = Column(String)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    
    metadata_relationship = relationship("Metadata", back_populates="players_info")
    

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(BigInteger, primary_key=True, autoincrement=True)   
    slp_version = Column(String)
    timer_type = Column(BigInteger)
    in_game_mode = Column(BigInteger)
    friendly_fire_enabled = Column(Boolean)
    is_teams = Column(Boolean)
    item_spawn_behavior = Column(BigInteger)
    stage_id = Column(BigInteger)
    starting_timer_seconds = Column(BigInteger)
    enabled_items = Column(BigInteger)
    scene = Column(BigInteger)
    game_mode = Column(BigInteger)
    language = Column(BigInteger)
    random_seed = Column(BigInteger)
    is_pal = Column(Boolean)
    is_frozen_ps = Column(Boolean)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="settings")

class HigherPortPlayerPostFrames(Base):
    __tablename__ = "higher_port_player_post_frames"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    frame = Column(BigInteger)
    player_index = Column(BigInteger)
    is_follower = Column(Boolean)
    internal_character_id = Column(BigInteger)
    action_state_id = Column(BigInteger)
    position_x = Column(Double)
    position_y = Column(Double)
    facing_direction = Column(BigInteger)
    percent = Column(Double)
    shield_size = Column(Double)
    last_attack_landed = Column(BigInteger)
    last_hit_by = Column(BigInteger)
    stocks_remaining = Column(BigInteger)
    action_state_counter = Column(Double)
    misc_action_state = Column(Double)
    is_airborne = Column(Boolean)
    last_ground_id = Column(BigInteger)
    jumps_remaining = Column(BigInteger)
    l_cancel_status = Column(BigInteger)
    hurtbox_collision_state = Column(BigInteger)
    hitlag_remaining = Column(BigInteger)
    animation_index = Column(BigInteger)
    self_induced_speeds_air_x = Column(Double)
    self_induced_speeds_y = Column(Double)
    self_induced_speeds_attack_x = Column(Double)
    self_induced_speeds_attack_y = Column(Double)
    self_induced_speeds_ground_x = Column(Double)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    


    metadata_relationship = relationship("Metadata", back_populates="higher_port_player_post_frames")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='higher_port_post_frames_to_metadata'),)

class LowerPortPlayerPostFrames(Base):
    __tablename__ = "lower_port_player_post_frames"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    frame = Column(BigInteger)
    player_index = Column(BigInteger)
    is_follower = Column(Boolean)
    internal_character_id = Column(BigInteger)
    action_state_id = Column(BigInteger)
    position_x = Column(Double)
    position_y = Column(Double)
    facing_direction = Column(BigInteger)
    percent = Column(Double)
    shield_size = Column(Double)
    last_attack_landed = Column(BigInteger)
    last_hit_by = Column(BigInteger)
    stocks_remaining = Column(BigInteger)
    action_state_counter = Column(Double)
    misc_action_state = Column(Double)
    is_airborne = Column(Boolean)
    last_ground_id = Column(BigInteger)
    jumps_remaining = Column(BigInteger)
    l_cancel_status = Column(BigInteger)
    hurtbox_collision_state = Column(BigInteger)
    hitlag_remaining = Column(BigInteger)
    animation_index = Column(BigInteger)
    self_induced_speeds_air_x = Column(Double)
    self_induced_speeds_y = Column(Double)
    self_induced_speeds_attack_x = Column(Double)
    self_induced_speeds_attack_y = Column(Double)
    self_induced_speeds_ground_x = Column(Double)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="lower_port_player_post_frames")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='lower_port_player_post_frames_to_metadata'),)

class HigherPortPlayerPreFrames(Base):
    __tablename__ = "higher_port_player_pre_frames"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    frame = Column(BigInteger)
    player_index = Column(BigInteger)
    is_follower = Column(Boolean)
    seed = Column(BigInteger)
    action_state_id = Column(BigInteger)
    position_x = Column(Double)
    position_y = Column(Double)
    facing_direction = Column(BigInteger)
    joy_stick_x = Column(Double)
    joy_stick_y = Column(Double)
    c_stick_x = Column(Double)
    c_stick_y = Column(Double)
    trigger = Column(Double)
    buttons = Column(BigInteger)
    physical_buttons = Column(BigInteger)
    physical_l_trigger = Column(Double)
    physical_r_trigger = Column(Double)
    raw_joy_stick_x = Column(BigInteger)
    percent = Column(Double)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="higher_port_player_pre_frames")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='higher_port_pre_frames_to_metadata'),)


class LowerPortPlayerPreFrames(Base):
    __tablename__ = "lower_port_player_pre_frames"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    frame = Column(BigInteger)
    player_index = Column(BigInteger)
    is_follower = Column(Boolean)
    seed = Column(BigInteger)
    action_state_id = Column(BigInteger)
    position_x = Column(Double)
    position_y = Column(Double)
    facing_direction = Column(BigInteger)
    joy_stick_x = Column(Double)
    joy_stick_y = Column(Double)
    c_stick_x = Column(Double)
    c_stick_y = Column(Double)
    trigger = Column(Double)
    buttons = Column(BigInteger)
    physical_buttons = Column(BigInteger)
    physical_l_trigger = Column(Double)
    physical_r_trigger = Column(Double)
    raw_joy_stick_x = Column(BigInteger)
    percent = Column(Double)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="lower_port_player_pre_frames")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='lower_port_pre_frames_to_metadata'),)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255))
    profile_picture = Column(String)

    uploaded_games = relationship('Metadata', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


engine = create_engine(database)

Base.metadata.create_all(engine)

