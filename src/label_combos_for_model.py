import pandas as pd
from sqlalchemy import create_engine
import sys, os, pdb, json
sys.path.append('..')
from src.database_info import database
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 1000)

json_data_filepath = 'player_uploads/d3_json_flowchart/json_data_for_frontend_visual.json'

def label_combos_for_model(game_id, engine, query):

    battlefield_x_axis = 228
    battlefield_y_axis_top_blastzone = 208
    battlefield_y_axis_bottom_blastzone = 113


    action_state_id_to_check_getting_hit = [0, 1, 2, 4, 8, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 227, 228, 239, 240, 241, 242]
    death_action_state_ids = [0, 1, 2, 4, 8]

    last_frame = None
    current_combo_id = 0
    higher_port_post_percent = 0.0
    lower_port_post_percent = 0.0

    successful_l_cancel = 1
    unsuccessful_l_cancel = 0
    no_l_cancel_on_frame = None
    
    df = pd.read_sql(query, engine, params=(game_id,))
    df['combo_block_for_model'] = None
    df['humanlabel'] = None
    df['attack_state_to_hit_in_combo_for_model'] =  None
    df['character_creating_combo_for_model'] = None
    df['lower_port_l_cancel_for_model'] = None
    df['higher_port_l_cancel_for_model'] = None
    df['lower_port_damage_done_with_combo'] = None
    df['higher_port_damage_done_with_combo'] = None
    df['lower_port_damage_done_with_combo_model_score'] = None
    df['higher_port_damage_done_with_combo_model_score'] = None
    df['higher_port_x_position_model_score'] = None
    df['higher_port_y_position_model_score'] = None
    df['lower_port_x_position_model_score'] = None
    df['lower_port_y_position_model_score'] = None
    df['higher_death_state_blocks'] = None
    df['lower_death_state_blocks'] = None

    for index, row in df.iterrows():
        current_frame = row['higher_post_frame'] 

        # Check for frame gaps to identify new combos
        if last_frame is not None and (current_frame - last_frame > 1):
            current_combo_id += 1

        # Label based on action_state_id
        if row["lower_post_action_state_id"] not in action_state_id_to_check_getting_hit:#lower port player creating combo
            df.at[index, 'combo_block_for_model'] = current_combo_id 
            df.at[index, 'character_creating_combo_for_model'] = 0

            if df.at[index, 'lower_post_internal_character_id'] == 1:
                df.at[index, 'humanlabel'] = 'fox'
            else:
                df.at[index, 'humanlabel'] = 'falco'


        elif row["higher_post_action_state_id"] not in action_state_id_to_check_getting_hit: #higher port player creating combo
            df.at[index, 'combo_block_for_model'] = current_combo_id 
            df.at[index, 'character_creating_combo_for_model'] = 1

            if df.at[index, 'higher_post_internal_character_id'] == 1:
                df.at[index, 'humanlabel'] = 'fox'
            else:
                df.at[index, 'humanlabel'] = 'falco'

        if row['lower_post_action_state_id'] in death_action_state_ids:
            lower_port_post_percent = 0.0
        
        if row['higher_post_action_state_id'] in death_action_state_ids:
            higher_port_post_percent = 0.0

        if row['lower_post_percent'] > lower_port_post_percent and row['lower_post_action_state_id'] not in death_action_state_ids:
            df.at[index, 'attack_state_to_hit_in_combo_for_model'] = row['higher_post_last_attack_landed']
            lower_port_post_percent = row['lower_post_percent']

        if row['higher_post_percent'] > higher_port_post_percent and row['higher_post_action_state_id'] not in death_action_state_ids:
            df.at[index, 'attack_state_to_hit_in_combo_for_model'] = row['lower_post_last_attack_landed']
            higher_port_post_percent = row['higher_post_percent']
        
        if row['lower_post_l_cancel_status'] == 0:
            df.at[index, 'lower_port_l_cancel_for_model'] = no_l_cancel_on_frame
        
        elif row['lower_post_l_cancel_status'] == 1:
            df.at[index, 'lower_port_l_cancel_for_model'] = successful_l_cancel
        
        elif row['lower_post_l_cancel_status'] == 2:
            df.at[index, 'lower_port_l_cancel_for_model'] = unsuccessful_l_cancel

        if row['higher_post_l_cancel_status'] == 0:
            df.at[index, 'higher_port_l_cancel_for_model'] = no_l_cancel_on_frame
        
        elif row['higher_post_l_cancel_status'] == 1:
            df.at[index, 'higher_port_l_cancel_for_model'] = successful_l_cancel
        
        elif row['higher_post_l_cancel_status'] == 2:
            df.at[index, 'higher_port_l_cancel_for_model'] = unsuccessful_l_cancel
        
        last_frame = current_frame

        #if the state of the frame before was not in the check to get hit frames and it is now in death action state
        #then we want to label this as dying not in hitstun, and we want to label the combo row as 

    grouped = df.groupby('combo_block_for_model')

    higher_port_previous_end_percent = 0.0
    lower_port_previous_end_percent = 0.0

    for name, group in grouped:
        # Skip the group if the combo block is marked as 'None'
        if pd.isna(group['combo_block_for_model'].iloc[0]):
            continue

        # Initialize variables to store start and end percents
        start_percent_higher = group['higher_post_percent'].iloc[0] + (higher_port_previous_end_percent - group['higher_post_percent'].iloc[0])
        end_percent_higher = group['higher_post_percent'].iloc[-1]
        start_percent_lower = group['lower_post_percent'].iloc[0] + (lower_port_previous_end_percent - group['lower_post_percent'].iloc[0])
        end_percent_lower = group['lower_post_percent'].iloc[-1]
        
        # Calculate damage done in the combo for each player
        damage_done_to_higher = end_percent_higher - start_percent_higher
        damage_done_to_lower = end_percent_lower - start_percent_lower
        
        # Store the damage done in the last row of the combo block'

        if damage_done_to_higher < 0:
            damage_done_to_higher = None
        
        if damage_done_to_lower < 0:
            damage_done_to_lower = None

        if damage_done_to_lower == 0:
            df.at[group.index[-1], 'higher_port_damage_done_with_combo'] = None

        else:
            df.at[group.index[-1], 'higher_port_damage_done_with_combo'] = damage_done_to_lower
        

        if damage_done_to_higher == 0:
            df.at[group.index[-1], 'lower_port_damage_done_with_combo'] = None

        else:
            df.at[group.index[-1], 'lower_port_damage_done_with_combo'] = damage_done_to_higher
        
        # Update the previous end percent for the next iteration
        higher_port_previous_end_percent = end_percent_higher
        lower_port_previous_end_percent = end_percent_lower

    #if the character creating the model is 0 then we grab the postion of the higher port, if the character creating the combo is 1 then grab the postion of the lower port

    for index, row in df.iterrows():

        lower_port_percent_damage_done = row['lower_port_damage_done_with_combo']
        higher_port_percent_damage_done = row['higher_port_damage_done_with_combo']

        if row['lower_port_damage_done_with_combo'] == None:
            df.at[index, 'lower_port_damage_done_with_combo_model_score'] = None
        
        else:
            df.at[index, 'lower_port_damage_done_with_combo_model_score'] = lower_port_percent_damage_done/100

        if row['higher_port_damage_done_with_combo'] == None:
            df.at[index, 'higher_port_damage_done_with_combo_model_score'] = None

        else:
            df.at[index, 'higher_port_damage_done_with_combo_model_score'] = higher_port_percent_damage_done/100




    # Create masks to identify death state blocks
    df['higher_death_state_blocks'] = df['higher_post_action_state_id'].isin(death_action_state_ids)
    df['lower_death_state_blocks'] = df['lower_post_action_state_id'].isin(death_action_state_ids)

    # Create a cumulative sum as a block id for consecutive death states
    df['higher_block_death_id'] = (~df['higher_death_state_blocks']).cumsum()
    df['lower_block_death_id'] = (~df['lower_death_state_blocks']).cumsum()

    # Get the first index of each death block for higher and lower death states
    first_higher_death_indices = df[df['higher_death_state_blocks']].groupby('higher_block_death_id').head(1).index
    first_lower_death_indices = df[df['lower_death_state_blocks']].groupby('lower_block_death_id').head(1).index

    # Keep only the first occurrence of each block
    df = df[(df.index.isin(first_higher_death_indices)) | (~df['higher_death_state_blocks'])]
    df = df[(df.index.isin(first_lower_death_indices)) | (~df['lower_death_state_blocks'])]

    columns_to_drop = ['higher_death_state_blocks', 'lower_death_state_blocks', 'higher_block_death_id', 'lower_block_death_id']

    # Drop the columns from the DataFrame
    df.drop(columns=columns_to_drop, inplace=True)

    last_rows = df.groupby('combo_block_for_model').tail(1)


    def update_position_score(row):

        if row['character_creating_combo_for_model'] == None:
            return row

        if row['character_creating_combo_for_model'] == 0:
            #then score the postion of the higher port character
            row['higher_port_x_position_model_score'] = abs(row['higher_post_position_x']) / battlefield_x_axis
            
            if row['higher_post_position_y'] < 0:
                row['higher_port_y_position_model_score'] = abs(row['higher_post_position_y']) / battlefield_y_axis_bottom_blastzone
            
            else:
                row['higher_port_y_position_model_score'] = abs(row['higher_post_position_y']) / battlefield_y_axis_top_blastzone
            
        elif row['character_creating_combo_for_model'] == 1:

            row['lower_port_x_position_model_score'] = abs(row['lower_post_position_x']) / battlefield_x_axis
            
            if row['lower_post_position_y'] < 0:
                row['lower_port_y_position_model_score'] = abs(row['lower_post_position_y']) / battlefield_y_axis_bottom_blastzone
            
            else:
                row['lower_port_y_position_model_score'] = abs(row['lower_post_position_y']) / battlefield_y_axis_top_blastzone
        
        return row

    last_rows = last_rows.apply(update_position_score, axis=1)


    df.update(last_rows)

    df.drop(df[pd.isna(df['combo_block_for_model'])].index, inplace=True)
    df = df.drop(columns=['humanlabel', 'higher_post_game_id', 'higher_post_last_attack_landed', 'lower_post_last_attack_landed'])
   
    
    return df


def transform_to_d3_json(df):
    d3_data = {'combos': {}}

    for combo_id, combo_group in df.groupby('combo_block_for_model'):
        nodes = combo_group.to_dict('records')

        links = [{'source': i, 'target': i+1} for i in range(len(nodes)-1)]

        d3_data['combos'][combo_id] = {'nodes': nodes, 'links': links}

    return d3_data


if __name__ == "__main__":

    engine = create_engine(database)

    query = '''SELECT higher_post_game_id, higher_post_frame, higher_post_internal_character_id, higher_post_action_state_id, higher_post_position_x, higher_post_position_y, 
        higher_post_facing_direction,higher_post_percent, higher_post_action_state_counter, higher_post_misc_action_state, higher_post_last_ground_id, higher_post_jumps_remaining,
        higher_post_l_cancel_status, higher_post_hitlag_remaining, higher_post_animation_index, higher_post_self_induced_speeds_air_x, higher_post_self_induced_speeds_y, 
        higher_post_self_induced_speeds_attack_x, higher_post_self_induced_speeds_attack_y, higher_post_self_induced_speeds_ground_x, higher_post_last_attack_landed, 
        lower_post_frame, lower_post_internal_character_id, lower_post_action_state_id, lower_post_position_x, lower_post_position_y, lower_post_facing_direction,
        lower_post_percent, lower_post_action_state_counter, lower_post_misc_action_state, lower_post_last_ground_id, lower_post_jumps_remaining,
        lower_post_l_cancel_status, lower_post_hitlag_remaining, lower_post_animation_index, lower_post_self_induced_speeds_air_x, lower_post_self_induced_speeds_y, 
        lower_post_self_induced_speeds_attack_x, lower_post_self_induced_speeds_attack_y, lower_post_self_induced_speeds_ground_x, lower_post_last_attack_landed 
        FROM combos_for_battlefield WHERE higher_post_game_id = %s ORDER BY higher_post_frame'''

    if os.environ.get('CALLED_FROM_FLASK') == '1':
        passed_game_id = sys.argv[1]
        df = label_combos_for_model(passed_game_id, engine, query)

        json_data_for_frontend_visual = transform_to_d3_json(df)
        
        with open(json_data_filepath, 'w') as f:
            json.dump(json_data_for_frontend_visual, f)


    else:
        meta_data_game_ids_query = 'SELECT game_id FROM melee_metadata'

        game_ids_df = pd.read_sql(meta_data_game_ids_query, engine)

        game_ids = game_ids_df['game_id'].tolist()

        for game_id in game_ids:
            df = label_combos_for_model(game_id, engine, query)

            csv_file = 'falco_vs_fox_csv_battlefield'

            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                df.to_csv(f, header=f.tell()==0, index=False)
