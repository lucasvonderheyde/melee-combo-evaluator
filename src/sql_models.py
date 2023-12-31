from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean, UniqueConstraint, BigInteger, Double, event
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from database_info import database
from werkzeug.security import generate_password_hash, check_password_hash
import re


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

    def serialize(self):
        return {
            'id': self.id,
            'slp_version': self.slp_version,
            'timer_type': self.timer_type,
            'in_game_mode': self.in_game_mode,
            'friendly_fire_enabled': self.friendly_fire_enabled,
            'is_teams': self.is_teams,
            'item_spawn_behavior': self.item_spawn_behavior,
            'stage_id': self.stage_id,
            'starting_timer_seconds': self.starting_timer_seconds,
            'enabled_items': self.enabled_items,
            'scene': self.scene,
            'game_mode': self.game_mode,
            'language': self.language,
            'random_seed': self.random_seed,
            'is_pal': self.is_pal,
            'is_frozen_ps': self.is_frozen_ps,
            'game_id': self.game_id
        }

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

    def serialize(self):
        return {
            'id': self.id,
            'player_index': self.player_index,
            'port': self.port,
            'character_id': self.character_id,
            'player_type': self.player_type,
            'start_stocks': self.start_stocks,
            'character_color': self.character_color,
            'team_shade': self.team_shade,
            'handicap': self.handicap,
            'team_id': self.team_id,
            'stamina_mode': self.stamina_mode,
            'silent_character': self.silent_character,
            'low_gravity': self.low_gravity,
            'invisible': self.invisible,
            'black_stock_icon': self.black_stock_icon,
            'metal': self.metal,
            'start_on_angel_platform': self.start_on_angel_platform,
            'rumble_enabled': self.rumble_enabled,
            'cpu_level': self.cpu_level,
            'offense_ratio': self.offense_ratio,
            'defense_ratio': self.defense_ratio,
            'model_scale': self.model_scale,
            'controller_fix': self.controller_fix,
            'name_tag': self.name_tag,
            'display_name': self.display_name,
            'connect_code': self.connect_code,
            'user_id': self.user_id,
            'game_id': self.game_id
        }


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

    # Existing fields
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255))
    profile_picture = Column(String)
    favorite_combo = Column(String)
    main_character = Column(String)
    secondary_character = Column(String)

    # Relationships
    uploaded_games = relationship('Metadata', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "favorite_combo": self.favorite_combo,
            "main_character": self.main_character,
            "secondary_character": self.secondary_character
            # Add other fields as needed
        }

    # Password methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Email validation function
def validate_email(target, value, oldvalue, initiator):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValueError("Invalid email format")

# Username validation function
def validate_username(target, value, oldvalue, initiator):
    if not re.match(r"^\w+$", value):  # Adjust regex as per your requirements
        raise ValueError("Invalid username format")

# Attaching listeners to the User model
event.listen(User.email, 'set', validate_email, retval=False)
event.listen(User.username, 'set', validate_username, retval=False)
    
engine = create_engine(database)

Base.metadata.create_all(engine)

