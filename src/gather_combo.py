import pandas as pd
from database_info import database, game_id, combo_table_select
from constants import stage_ids
import psycopg2

def move_combo_data_to_proper_stage():
    
    connection = psycopg2.connect(database)

    cursor = connection.cursor()

    cursor.execute(f"SELECT stage_id FROM settings WHERE game_id = %s", [game_id])
    stage_id = cursor.fetchone()[0]


    combo_table = None
    for key, value in stage_ids.items():
        if key == stage_id:
            combo_table = f"combos_for_{value}"
            break

    
    if combo_table:
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {combo_table} AS 
                {combo_table_select}    
            ''', [game_id])
        

    cursor.execute(f'''INSERT INTO {combo_table} (
            higher_post_id,
            higher_post_frame,
            higher_post_player_index, 
            higher_post_is_follower,
            higher_post_internal_character_id,
            higher_post_action_state_id,
            higher_post_position_x,
            higher_post_position_y,
            higher_post_facing_direction,
            higher_post_percent,
            higher_post_shield_size,
            higher_post_last_attack_landed,
            higher_post_last_hit_by,
            higher_post_stocks_remaining,
            higher_post_action_state_counter,
            higher_post_misc_action_state,
            higher_post_is_airborne,
            higher_post_last_ground_id,
            higher_post_jumps_remaining,
            higher_post_l_cancel_status,
            higher_post_hurtbox_collision_state,
            higher_post_hitlag_remaining,
            higher_post_animation_index,
            higher_post_self_induced_speeds_air_x,
            higher_post_self_induced_speeds_y,
            higher_post_self_induced_speeds_attack_x,
            higher_post_self_induced_speeds_attack_y,
            higher_post_self_induced_speeds_ground_x,
            higher_post_game_id,
            higher_pre_id,
            higher_pre_frame,
            higher_pre_player_index,
            higher_pre_is_follower,
            higher_pre_seed,
            higher_pre_action_state_id,
            higher_pre_position_x,
            higher_pre_position_y,
            higher_pre_facing_direction,
            higher_pre_joy_stick_x,
            higher_pre_joy_stick_y,
            higher_pre_c_stick_x,
            higher_pre_c_stick_y,
            higher_pre_trigger,
            higher_pre_buttons,
            higher_pre_physical_buttons,
            higher_pre_physical_l_trigger,
            higher_pre_physical_r_trigger,
            higher_pre_raw_joy_stick_x,
            higher_pre_percent,
            higher_pre_game_id,
            lower_post_id,
            lower_post_frame,
            lower_post_player_index,
            lower_post_is_follower,
            lower_post_internal_character_id,
            lower_post_action_state_id,
            lower_post_position_x,
            lower_post_position_y,
            lower_post_facing_direction,
            lower_post_percent,
            lower_post_shield_size,
            lower_post_last_attack_landed,
            lower_post_last_hit_by,
            lower_post_stocks_remaining,
            lower_post_action_state_counter,
            lower_post_misc_action_state,
            lower_post_is_airborne,
            lower_post_last_ground_id,
            lower_post_jumps_remaining,
            lower_post_l_cancel_status,
            lower_post_hurtbox_collision_state,
            lower_post_hitlag_remaining,
            lower_post_animation_index,
            lower_post_self_induced_speeds_air_x,
            lower_post_self_induced_speeds_y,
            lower_post_self_induced_speeds_attack_x,
            lower_post_self_induced_speeds_attack_y,
            lower_post_self_induced_speeds_ground_x,
            lower_post_game_id,
            lower_pre_id,
            lower_pre_frame,
            lower_pre_player_index,
            lower_pre_is_follower,
            lower_pre_seed,
            lower_pre_action_state_id,
            lower_pre_position_x,
            lower_pre_position_y,
            lower_pre_facing_direction,
            lower_pre_joy_stick_x,
            lower_pre_joy_stick_y,
            lower_pre_c_stick_x,
            lower_pre_c_stick_y,
            lower_pre_trigger,
            lower_pre_buttons,
            lower_pre_physical_buttons,
            lower_pre_physical_l_trigger,
            lower_pre_physical_r_trigger,
            lower_pre_raw_joy_stick_x,
            lower_pre_percent,
            lower_pre_game_id)
            {combo_table_select}''', [game_id])
    
    connection.commit()

    cursor.close()
    connection.close()
    
move_combo_data_to_proper_stage()
