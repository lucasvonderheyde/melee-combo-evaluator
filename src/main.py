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


    directory_path = "../../test/jsondb/output_folder_1697054420015"

    for filename in os.listdir(directory_path):

        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)

            if "settings" in filename:
                with open(filepath, "r") as incomingSettings:
                    settingsData = json.load(incomingSettings)

            elif "all_post_frames" in filename:
                df_post_frames = pd.read_json(filepath)
                
            elif "metadata" in filename:
                df_metadata = pd.read_json(filepath)



    filtered_settings_data = {key: value for key, value in settingsData.items() if not isinstance(value, (dict, list))}
    settings_top_level_df = pd.DataFrame([filtered_settings_data]) 


    top_level_settings = pd.DataFrame([settingsData])
    df_game_info = pd.DataFrame([settingsData.get('gameInfoBlock', {})])
    df_match_info = pd.DataFrame([settingsData.get('matchInfo', {})])
    df_players_info = pd.DataFrame(settingsData.get('players', []))

    filtered_metadata_df = df_metadata[['startAt', 'lastFrame', 'playedOn']].copy()


    lower_port_player_df = pd.json_normalize(df_post_frames['lowerPortPlayerPostFrame'])
    higher_port_player_df = pd.json_normalize(df_post_frames['higherPortPlayerPostFrame'])


    lower_port_post_frames_columns_to_remove = []
    higher_port_post_frames_columns_to_remove = []

    lower_port_post_frames_columns_to_remove.append("currentComboCount")
    higher_port_post_frames_columns_to_remove.append("currentComboCount")

    lower_port_is_follower_first_value = lower_port_player_df['isFollower'].iloc[0]
    higher_port_is_follower_first_value = higher_port_player_df['isFollower'].iloc[0]

    if lower_port_is_follower_first_value == False:
        lower_port_post_frames_columns_to_remove.append('isFollower')

    else:
        pass

    if higher_port_is_follower_first_value == False:
        higher_port_post_frames_columns_to_remove.append('isFollower')

    else:
        pass


    filtered_lower_port_player_df = lower_port_player_df.drop(columns=lower_port_post_frames_columns_to_remove, axis=1)
    filtered_higher_port_player_df = higher_port_player_df.drop(columns=higher_port_post_frames_columns_to_remove, axis=1)

    game_id = uuid.uuid4()

    # Find character names based on their IDs
    lower_port_character_id = filtered_lower_port_player_df['internalCharacterId'].iloc[0]
    higher_port_character_id = filtered_higher_port_player_df['internalCharacterId'].iloc[0]

    lower_port_character_name = internal_character_ids.get(lower_port_character_id, "Unknown")
    higher_port_character_name = internal_character_ids.get(higher_port_character_id, "Unknown")

    # Sorting character names for consistent schema naming
    list_to_sort_character_names = sorted([lower_port_character_name, higher_port_character_name])

    # Form the schema name
    schema_name = f"{list_to_sort_character_names[0]}_vs_{list_to_sort_character_names[1]}"

    # Add the unique game_id to each DataFrame
    filtered_higher_port_player_df['game_id'] = game_id
    filtered_lower_port_player_df['game_id'] = game_id
    filtered_metadata_df['game_id'] = game_id
    settings_top_level_df['game_id'] = game_id
    df_game_info['game_id'] = game_id
    df_players_info['game_id'] = game_id
    df_match_info['game_id'] = game_id

    # Send DataFrames to the database under the defined schema
    filtered_higher_port_player_df.to_sql(name=f"higher_port_player {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
    filtered_lower_port_player_df.to_sql(name=f"lower_port_player {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
    filtered_metadata_df.to_sql(name=f"metadata {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
    settings_top_level_df.to_sql(name=f"settings {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
    df_game_info.to_sql(name=f"game_info {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
    df_players_info.to_sql(name=f"players_info {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)
    df_match_info.to_sql(name=f"match_info {game_id}", con=engine, if_exists="replace", index=True, schema=schema_name)

if __name__ == "__main__":
    main()