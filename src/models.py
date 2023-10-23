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
    higher_port_player_post_frames = relationship("HigherPortPlayerPostFrames", back_populates="metadata_relationship")
    lower_port_player_post_frames = relationship("LowerPortPlayerPostFrames", back_populates="metadata_relationship")
    higher_port_player_pre_frames = relationship("HigherPortPlayerPreFrames", back_populates="metadata_relationship")
    lower_port_player_pre_frames = relationship("LowerPortPlayerPreFrames", back_populates="metadata_relationship")

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
    player_type = Column(Integer)
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
    slp_version = Column(String)
    timer_type = Column(Integer)
    in_game_mode = Column(Integer)
    friendly_fire_enabled = Column(Boolean)
    is_teams = Column(Boolean)
    item_spawn_behavior = Column(Integer)
    stage_id = Column(Integer)
    starting_timer_seconds = Column(Integer)
    enabled_items = Column(Integer)
    scene = Column(Integer)
    game_mode = Column(Integer)
    language = Column(Integer)
    random_seed = Column(Integer)
    is_pal = Column(Boolean)
    is_frozen_ps = Column(Boolean)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))


    metadata_relationship = relationship("Metadata", back_populates="settings")

class HigherPortPlayerPostFrames(Base):
    __tablename__ = "higher_port_player_post_frames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame = Column(Integer)
    player_index = Column(Integer)
    is_follower = Column(Boolean)
    internal_character_id = Column(Integer)
    action_state_id = Column(Integer)
    position_x = Column(Float)
    position_y = Column(Float)
    facing_direction = Column(Integer)
    percent = Column(Float)
    shield_size = Column(Float)
    last_attack_landed = Column(Integer)
    last_hit_by = Column(Integer)
    stocks_remaining = Column(Integer)
    action_state_counter = Column(Float)
    misc_action_state = Column(Float)
    is_airborne = Column(Boolean)
    last_ground_id = Column(Integer)
    jumps_remaining = Column(Integer)
    l_cancel_status = Column(Integer)
    hurtbox_collision_state = Column(Integer)
    hitlag_remaining = Column(Integer)
    animation_index = Column(Integer)
    self_induced_speeds_air_x = Column(Float)
    self_induced_speeds_y = Column(Float)
    self_induced_speed_attack_x = Column(Float)
    self_induced_speed_attack_y = Column(Float)
    self_induced_speed_ground_x = Column(Float)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))
    


    metadata_relationship = relationship("Metadata", back_populates="higher_port_player_post_frames")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='higher_port_post_frames_to_metadata'),)

class LowerPortPlayerPostFrames(Base):
    __tablename__ = "lower_port_player_post_frames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame = Column(Integer)
    player_index = Column(Integer)
    is_follower = Column(Boolean)
    internal_character_id = Column(Integer)
    action_state_id = Column(Integer)
    position_x = Column(Float)
    position_y = Column(Float)
    facing_direction = Column(Integer)
    percent = Column(Float)
    shield_size = Column(Float)
    last_attack_landed = Column(Integer)
    last_hit_by = Column(Integer)
    stocks_remaining = Column(Integer)
    action_state_counter = Column(Float)
    misc_action_state = Column(Float)
    is_airborne = Column(Boolean)
    last_ground_id = Column(Integer)
    jumps_remaining = Column(Integer)
    l_cancel_status = Column(Integer)
    hurtbox_collision_state = Column(Integer)
    hitlag_remaining = Column(Integer)
    animation_index = Column(Integer)
    self_induced_speeds_air_x = Column(Float)
    self_induced_speeds_y = Column(Float)
    self_induced_speed_attack_x = Column(Float)
    self_induced_speed_attack_y = Column(Float)
    self_induced_speed_ground_x = Column(Float)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="lower_port_player_post_frames")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='lower_port_player_post_frames_to_metadata'),)

class HigherPortPlayerPreFrames(Base):
    __tablename__ = "higher_port_player_pre_frames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame = Column(Integer)
    player_index = Column(Integer)
    is_follower = Column(Boolean)
    seed = Column(Integer)
    action_state_id = Column(Integer)
    position_x = Column(Float)
    position_y = Column(Float)
    facing_direction = Column(Integer)
    joy_stick_x = Column(Float)
    joy_stick_y = Column(Float)
    c_stick_x = Column(Float)
    c_stick_y = Column(Float)
    trigger = Column(Float)
    buttons = Column(Integer)
    physical_buttons = Column(Integer)
    physical_l_trigger = Column(Float)
    physical_r_trigger = Column(Float)
    raw_joy_stick_x = Column(Integer)
    percent = Column(Float)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="higher_port_player_pre_frames")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='higher_port_pre_frames_to_metadata'),)


class LowerPortPlayerPreFrames(Base):
    __tablename__ = "lower_port_player_pre_frames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame = Column(Integer)
    player_index = Column(Integer)
    is_follower = Column(Boolean)
    seed = Column(Integer)
    action_state_id = Column(Integer)
    position_x = Column(Float)
    position_y = Column(Float)
    facing_direction = Column(Integer)
    joy_stick_x = Column(Float)
    joy_stick_y = Column(Float)
    c_stick_x = Column(Float)
    c_stick_y = Column(Float)
    trigger = Column(Float)
    buttons = Column(Integer)
    physical_buttons = Column(Integer)
    physical_l_trigger = Column(Float)
    physical_r_trigger = Column(Float)
    raw_joy_stick_x = Column(Integer)
    percent = Column(Float)
    game_id = Column(String, ForeignKey('melee_metadata.game_id'))

    metadata_relationship = relationship("Metadata", back_populates="lower_port_player_pre_frames")
    __table_args__ = (UniqueConstraint('game_id', 'frame', name='lower_port_pre_frames_to_metadata'),)

engine = create_engine(f'postgresql://{username}:{password}@localhost/Melee_Combo_Database')

Base.metadata.create_all(engine)