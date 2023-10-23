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

    settings_df, post_frames_df, metadata_df = get_slippi_game_output_data("../test/jsondb/output_folder_1697054420015")


    filtered_settings_data = {key: value for key, value in settings_df.items() if not isinstance(value, (dict, list))}
    settings_top_level_df = pd.DataFrame([filtered_settings_data]) 

    game_info_df = pd.DataFrame([settings_df.get('gameInfoBlock', {})])
    match_info_df = pd.DataFrame([settings_df.get('matchInfo', {})])
    players_info_df = pd.DataFrame(settings_df.get('players', []))
    
    filtered_metadata_df = metadata_df[['startAt', 'lastFrame', 'playedOn']].copy()


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


    game_metadata.game_info = [game_info]




    session.add(game_metadata)
    session.commit()





    # lower_port_player_df = pd.json_normalize(post_frames_df['lowerPortPlayerPostFrame'])

    # filtered_lower_port_player_df = remove_is_follower_lower_port(lower_port_player_df)
    # filtered_lower_port_player_df.drop("currentComboCount", axis=1)


    # higher_port_player_df = pd.json_normalize(post_frames_df['higherPortPlayerPostFrame'])

    # filtered_higher_port_player_df = remove_is_follower_higher_port(higher_port_player_df)
    # filtered_higher_port_player_df.drop("currentComboCount", axis=1, inplace=True)
    

    # alphabetical_sort_into_matchup = sorted([get_lower_port_character_name_for_sorting(filtered_lower_port_player_df), get_lower_port_character_name_for_sorting(filtered_higher_port_player_df)])

    # schema_name = f"{alphabetical_sort_into_matchup[0]}_vs_{alphabetical_sort_into_matchup[1]}"




def get_slippi_game_output_data(directory_path):
    settings_df = pd.DataFrame()
    post_frames_df =  pd.DataFrame()
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
    
    return settings_df, post_frames_df, metadata_df


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
   

def remove_is_follower_lower_port(lower_port_player_df):
    
    is_follower_first_value = lower_port_player_df['isFollower'].iloc[0]

    return get_does_player_have_follower(is_follower_first_value, lower_port_player_df)


def remove_is_follower_higher_port(higher_port_player_df):

    is_follower_first_value = higher_port_player_df['isFollower'].iloc[0]

    return get_does_player_have_follower(is_follower_first_value, higher_port_player_df)


def get_does_player_have_follower(is_follower_first_value, player_df):
    if is_follower_first_value == False:
        player_df.drop('isFollower', axis=1, inplace=True)

    else:
        pass

    return player_df

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