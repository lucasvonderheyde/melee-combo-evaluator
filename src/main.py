import json
import os
import pandas as pd
from sqlalchemy import create_engine
from constants import internal_character_ids
import uuid


def main():
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 35)

    settings_df, post_frames_df, metadata_df = get_slippi_game_output_data("../test/jsondb/output_folder_1697054420015")


    filtered_settings_data = {key: value for key, value in settings_df.items() if not isinstance(value, (dict, list))}
    settings_top_level_df = pd.DataFrame([filtered_settings_data]) 

    df_game_info = pd.DataFrame([settings_df.get('gameInfoBlock', {})])
    df_match_info = pd.DataFrame([settings_df.get('matchInfo', {})])
    df_players_info = pd.DataFrame(settings_df.get('players', []))
    

    filtered_metadata_df = metadata_df[['startAt', 'lastFrame', 'playedOn']].copy()

    lower_port_player_df = pd.json_normalize(post_frames_df['lowerPortPlayerPostFrame'])

    filtered_lower_port_player_df = remove_is_follower_lower_port(lower_port_player_df)
    filtered_lower_port_player_df.drop("currentComboCount", axis=1)


    higher_port_player_df = pd.json_normalize(post_frames_df['higherPortPlayerPostFrame'])

    filtered_higher_port_player_df = remove_is_follower_higher_port(higher_port_player_df)
    filtered_higher_port_player_df.drop("currentComboCount", axis=1, inplace=True)

    print(filtered_higher_port_player_df)
#### this is where all of the posting logic will go still hase to be refactoreed##

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




# game_id = uuid.uuid4()

# # Find character names based on their IDs
# lower_port_character_id = filtered_lower_port_player_df['internalCharacterId'].iloc[0]
# higher_port_character_id = filtered_higher_port_player_df['internalCharacterId'].iloc[0]

# lower_port_character_name = internal_character_ids.get(lower_port_character_id, "Unknown")
# higher_port_character_name = internal_character_ids.get(higher_port_character_id, "Unknown")

# # Sorting character names for consistent schema naming
# list_to_sort_character_names = sorted([lower_port_character_name, higher_port_character_name])

# # Form the schema name
# schema_name = f"{list_to_sort_character_names[0]}_vs_{list_to_sort_character_names[1]}"

# # Add the unique game_id to each DataFrame
# filtered_higher_port_player_df['game_id'] = game_id
# filtered_lower_port_player_df['game_id'] = game_id
# filtered_metadata_df['game_id'] = game_id
# settings_top_level_df['game_id'] = game_id
# df_game_info['game_id'] = game_id
# df_players_info['game_id'] = game_id
# df_match_info['game_id'] = game_id

# # Send DataFrames to the database under the defined schema
# filtered_higher_port_player_df.to_sql(name=f"higher_port_player {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
# filtered_lower_port_player_df.to_sql(name=f"lower_port_player {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
# filtered_metadata_df.to_sql(name=f"metadata {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
# settings_top_level_df.to_sql(name=f"settings {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
# df_game_info.to_sql(name=f"game_info {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
# df_players_info.to_sql(name=f"players_info {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
# df_match_info.to_sql(name=f"match_info {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)

if __name__ == "__main__":
    main()