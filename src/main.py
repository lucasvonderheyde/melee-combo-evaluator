import json
import uuid
import os
import pdb

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_info import username, password
from models import Metadata, GameInfo, MatchInfo, PlayersInfo, Settings, HigherPortPlayerPostFrames, LowerPortPlayerPostFrames, HigherPortPlayerPreFrames, LowerPortPlayerPreFrames

def main():
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 35)

    game_id = uuid.uuid4()
    engine = create_engine(f'postgresql://{username}:{password}@localhost/Melee_Combo_Database')

    Session = sessionmaker(bind=engine)
    session = Session() 

    settings_df, post_frames_df, pre_frames_df, metadata_df = get_slippi_game_output_data("../data/temp_json_data/output_folder_1698097200272")


    filtered_settings_data = {key: value for key, value in settings_df.items() if not isinstance(value, (dict, list))}
    settings_top_level_df = pd.DataFrame([filtered_settings_data]) 

    game_info_df = pd.DataFrame([settings_df.get('gameInfoBlock', {})])
    match_info_df = pd.DataFrame([settings_df.get('matchInfo', {})])
    players_info_df = pd.DataFrame(settings_df.get('players', []))
    
    filtered_metadata_df = metadata_df[['startAt', 'lastFrame', 'playedOn']].copy()

    lower_port_player_post_frames_df = pd.json_normalize(post_frames_df['lowerPortPlayerPostFrame'])
    lower_port_player_post_frames_df.drop("currentComboCount", axis=1)

    higher_port_player_post_frames_df = pd.json_normalize(post_frames_df['higherPortPlayerPostFrame'])
    higher_port_player_post_frames_df.drop("currentComboCount", axis=1, inplace=True)

    lower_port_player_pre_frames_df = pd.json_normalize(pre_frames_df['lowerPortPlayerPreFrame'])
    higher_port_player_pre_frames_df = pd.json_normalize(pre_frames_df['higherPortPlayerPreFrame'])


    game_metadata = Metadata(

        game_id = str(game_id),
        start_at = filtered_metadata_df['startAt'].iloc[0],
        last_frame = int(filtered_metadata_df['lastFrame'].iloc[0]),
        played_on = filtered_metadata_df['playedOn'].iloc[0] 
    )

    game_info = GameInfo(

        game_bit_field_1 = int(game_info_df['gameBitfield1'].iloc[0]),
        game_bit_field_2 = int(game_info_df['gameBitfield2'].iloc[0]),
        game_bit_field_3 = int(game_info_df['gameBitfield3'].iloc[0]),
        game_bit_field_4 = int(game_info_df['gameBitfield4'].iloc[0]),
        bomb_rain_enabled = bool(game_info_df['bombRainEnabled'].iloc[0]),
        item_spawn_behavior = int(game_info_df['itemSpawnBehavior'].iloc[0]),
        self_destruct_score_value = int(game_info_df['selfDestructScoreValue'].iloc[0]),
        item_spawn_bit_field_1 = int(game_info_df['itemSpawnBitfield1'].iloc[0]),
        item_spawn_bit_field_2 = int(game_info_df['itemSpawnBitfield2'].iloc[0]),
        item_spawn_bit_field_3 = int(game_info_df['itemSpawnBitfield3'].iloc[0]),
        item_spawn_bit_field_4 = int(game_info_df['itemSpawnBitfield4'].iloc[0]),
        item_spawn_bit_field_5 = int(game_info_df['itemSpawnBitfield5'].iloc[0]),
        damage_ratio = int(game_info_df['damageRatio'].iloc[0]),
        game_id = str(game_id)
    )

    match_info = MatchInfo(
        match_id = str(match_info_df['matchId'].iloc[0]),
        game_number = int(match_info_df['gameNumber'].iloc[0]),
        tiebreaker_number = int(match_info_df['tiebreakerNumber'].iloc[0]),
        game_id = str(game_id)
    )

    settings_info = Settings(
    
        slp_version = str(settings_top_level_df['slpVersion'].iloc[0]),
        timer_type = int(settings_top_level_df['timerType'].iloc[0]),
        in_game_mode = int(settings_top_level_df['inGameMode'].iloc[0]),
        friendly_fire_enabled = bool(settings_top_level_df['friendlyFireEnabled'].iloc[0]),
        is_teams = bool(settings_top_level_df['isTeams'].iloc[0]),
        item_spawn_behavior = int(settings_top_level_df['itemSpawnBehavior'].iloc[0]),
        stage_id = int(settings_top_level_df['stageId'].iloc[0]),
        starting_timer_seconds = int(settings_top_level_df['startingTimerSeconds'].iloc[0]),
        enabled_items = int(settings_top_level_df['enabledItems'].iloc[0]),
        scene = int(settings_top_level_df['scene'].iloc[0]),
        game_mode = int(settings_top_level_df['gameMode'].iloc[0]),
        language = int(settings_top_level_df['language'].iloc[0]),
        random_seed = int(settings_top_level_df['randomSeed'].iloc[0]),
        is_pal = bool(settings_top_level_df['isPAL'].iloc[0]),
        is_frozen_ps = bool(settings_top_level_df['isFrozenPS'].iloc[0]),
        game_id = str(game_id)
    )

    for index, row in players_info_df.iterrows():
        players_info = PlayersInfo(
            player_index = int(row['playerIndex']),
            port = int(row['port']),
            character_id = int(row['characterId']),
            player_type = int(row['type']),
            start_stocks = int(row['startStocks']),
            character_color = int(row['characterColor']),
            team_shade = int(row['teamShade']),
            handicap = int(row['handicap']),
            team_id = int(row['teamId']),
            stamina_mode = int(row['staminaMode']),
            silent_character = int(row['silentCharacter']),
            low_gravity = bool(row['lowGravity']),
            invisible = bool(row['invisible']),
            black_stock_icon = bool(row['blackStockIcon']),
            metal = bool(row['metal']),
            start_on_angel_platform = bool(row['startOnAngelPlatform']),
            rumble_enabled = bool(row['rumbleEnabled']),
            cpu_level = int(row['cpuLevel']),
            offense_ratio = int(row['offenseRatio']),
            defense_ratio = int(row['defenseRatio']),
            model_scale = int(row['modelScale']),
            controller_fix = str(row['controllerFix']),
            name_tag = str(row['nametag']),
            display_name = str(row['displayName']),
            connect_code = str(row['connectCode']),
            user_id = str(row['userId']),
            game_id = str(game_id)
        )
        session.add(players_info)

    for index, row in lower_port_player_post_frames_df.iterrows():
        lower_port_player_post_frames_info = LowerPortPlayerPostFrames(

            frame = int(row['frame']),
            player_index = int(row['playerIndex']),
            is_follower = bool(row['isFollower']),
            internal_character_id = int(row['internalCharacterId']),
            action_state_id = int(row['actionStateId']),
            position_x = float(row['positionX']),
            position_y = float(row['positionY']),
            facing_direction = int(row['facingDirection']),
            percent = float(row['percent']),
            shield_size = float(row['shieldSize']),
            last_attack_landed = int(row['lastAttackLanded']),
            last_hit_by = int(row['lastHitBy']),
            stocks_remaining = int(row['stocksRemaining']),
            action_state_counter = float(row['actionStateCounter']),
            misc_action_state = float(row['miscActionState']),
            is_airborne = bool(row['isAirborne']),
            last_ground_id = int(row['lastGroundId']),
            jumps_remaining = int(row['jumpsRemaining']),
            l_cancel_status = int(row['lCancelStatus']),
            hurtbox_collision_state = int(row['hurtboxCollisionState']),
            hitlag_remaining = int(row['hitlagRemaining']),
            animation_index = int(row['animationIndex']),
            self_induced_speeds_air_x = float(row['selfInducedSpeeds.airX']),
            self_induced_speeds_y = float(row['selfInducedSpeeds.y']),
            self_induced_speeds_attack_x = float(row['selfInducedSpeeds.attackX']),
            self_induced_speeds_attack_y = float(row['selfInducedSpeeds.attackY']),
            self_induced_speeds_ground_x = float(row['selfInducedSpeeds.groundX']),
            game_id = str(game_id)
        )
        session.add(lower_port_player_post_frames_info)

    for index, row in higher_port_player_post_frames_df.iterrows():
        higher_port_player_post_frames_info = HigherPortPlayerPostFrames(

            frame = int(row['frame']),
            player_index = int(row['playerIndex']),
            is_follower = bool(row['isFollower']),
            internal_character_id = int(row['internalCharacterId']),
            action_state_id = int(row['actionStateId']),
            position_x = float(row['positionX']),
            position_y = float(row['positionY']),
            facing_direction = int(row['facingDirection']),
            percent = float(row['percent']),
            shield_size = float(row['shieldSize']),
            last_attack_landed = int(row['lastAttackLanded']),
            last_hit_by = int(row['lastHitBy']),
            stocks_remaining = int(row['stocksRemaining']),
            action_state_counter = float(row['actionStateCounter']),
            misc_action_state = float(row['miscActionState']),
            is_airborne = bool(row['isAirborne']),
            last_ground_id = int(row['lastGroundId']),
            jumps_remaining = int(row['jumpsRemaining']),
            l_cancel_status = int(row['lCancelStatus']),
            hurtbox_collision_state = int(row['hurtboxCollisionState']),
            hitlag_remaining = int(row['hitlagRemaining']),
            animation_index = int(row['animationIndex']),
            self_induced_speeds_air_x = float(row['selfInducedSpeeds.airX']),
            self_induced_speeds_y = float(row['selfInducedSpeeds.y']),
            self_induced_speeds_attack_x = float(row['selfInducedSpeeds.attackX']),
            self_induced_speeds_attack_y = float(row['selfInducedSpeeds.attackY']),
            self_induced_speeds_ground_x = float(row['selfInducedSpeeds.groundX']),
            game_id = str(game_id)
        )
        session.add(higher_port_player_post_frames_info)


    for index, row in lower_port_player_pre_frames_df.iterrows():
        lower_port_player_pre_frames_info = LowerPortPlayerPreFrames(

            frame = int(row['frame']),
            player_index = int(row['playerIndex']),
            is_follower = bool(row['isFollower']),
            seed = int(row['seed']),
            action_state_id = int(row['actionStateId']),
            position_x = float(row['positionX']),
            position_y = float(row['positionY']),
            facing_direction = int(row['facingDirection']),
            joy_stick_x = float(row['joystickX']),
            joy_stick_y = float(row['joystickY']),
            c_stick_x = float(row['cStickX']),
            c_stick_y = float(row['cStickY']),
            trigger = float(row['trigger']),
            buttons = int(row['buttons']),
            physical_buttons = int(row['physicalButtons']),
            physical_l_trigger = float(row['physicalLTrigger']),
            physical_r_trigger = float(row['physicalRTrigger']),
            raw_joy_stick_x = int(row['rawJoystickX']),
            percent = float(row['percent']),
            game_id = str(game_id)
        )
        session.add(lower_port_player_pre_frames_info)


    for index, row in higher_port_player_pre_frames_df.iterrows():
        higher_port_player_pre_frames_info = HigherPortPlayerPreFrames(

            frame = int(row['frame']),
            player_index = int(row['playerIndex']),
            is_follower = bool(row['isFollower']),
            seed = int(row['seed']),
            action_state_id = int(row['actionStateId']),
            position_x = float(row['positionX']),
            position_y = float(row['positionY']),
            facing_direction = int(row['facingDirection']),
            joy_stick_x = float(row['joystickX']),
            joy_stick_y = float(row['joystickY']),
            c_stick_x = float(row['cStickX']),
            c_stick_y = float(row['cStickY']),
            trigger = float(row['trigger']),
            buttons = int(row['buttons']),
            physical_buttons = int(row['physicalButtons']),
            physical_l_trigger = float(row['physicalLTrigger']),
            physical_r_trigger = float(row['physicalRTrigger']),
            raw_joy_stick_x = int(row['rawJoystickX']),
            percent = float(row['percent']),
            game_id = str(game_id)
    )
    session.add(higher_port_player_pre_frames_info)


    session.add(settings_info)
    session.add(match_info)
    session.add(game_info)
    session.add(game_metadata)
    session.commit()





    

    # alphabetical_sort_into_matchup = sorted([get_lower_port_character_name_for_sorting(filtered_lower_port_player_df), get_lower_port_character_name_for_sorting(filtered_higher_port_player_df)])

    # schema_name = f"{alphabetical_sort_into_matchup[0]}_vs_{alphabetical_sort_into_matchup[1]}"




def get_slippi_game_output_data(directory_path):
    settings_df = pd.DataFrame()
    post_frames_df =  pd.DataFrame()
    pre_frames_df = pd.DataFrame()
    metadata_df =  pd.DataFrame()
    
    for filename in os.listdir(directory_path):

        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)

            if "settings" in filename:
                with open(filepath, "r") as incomingSettings:
                    settings_df = json.load(incomingSettings)

            elif "all_post_frames" in filename:
                post_frames_df = pd.read_json(filepath)
                
            elif "metadata" in filename:
                metadata_df = pd.read_json(filepath)

            elif "all_pre_frames" in filename:
                pre_frames_df = pd.read_json(filepath)
    
    return settings_df, post_frames_df, pre_frames_df, metadata_df


def normalize_top_level_settings_data(settings_df):

    filtered_settings_data = {key: value for key, value in settings_df.items() if not isinstance(value, (dict, list))}
    settings_top_level_df = pd.DataFrame([filtered_settings_data]) 

    return filtered_settings_data, settings_top_level_df


def structure_and_divide_settings(settings_df):

    df_game_info = pd.DataFrame([settings_df.get('gameInfoBlock', {})])
    df_match_info = pd.DataFrame([settings_df.get('matchInfo', {})])
    df_players_info = pd.DataFrame(settings_df.get('players', []))

    return df_game_info, df_match_info, df_players_info


def filter_metadata(df_metadata):

    filtered_metadata_df = df_metadata[['startAt', 'lastFrame', 'playedOn']].copy()

    return filtered_metadata_df
   

def get_lower_port_character_name_for_sorting(filtered_lower_port_player_df):
    lower_port_character_id = filtered_lower_port_player_df['internalCharacterId'].iloc[0]
    
    return internal_character_ids.get(lower_port_character_id, "Unknown")    

def get_lower_port_character_name_for_sorting(filtered_higher_port_player_df):
    higher_port_character_id = filtered_higher_port_player_df['internalCharacterId'].iloc[0]
    
    return internal_character_ids.get(higher_port_character_id, "Unknown")

def post_df(df, df_name, game_id, engine, schema_name):
    df['game_id'] = game_id
    df.to_sql(name=f"{df_name} {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)

if __name__ == "__main__":
    main()