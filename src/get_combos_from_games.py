import pandas as pd
from database_info import database, game_id, combo_table_columns_to_post_to_db, select_combo_data_for_table
from constants import stage_ids
import psycopg2

def move_combo_data_to_proper_stage():
    try:
        connection = psycopg2.connect(database)
        cursor = connection.cursor()

        cursor.execute("SELECT stage_id FROM settings WHERE game_id = %s", (game_id,))
        result = cursor.fetchone()

        if result is None:
            raise ValueError("No stage_id found for the given game_id. Aborting operation.")

        stage_id = result[0]
        print(stage_id)
        combo_table = None
        for key, value in stage_ids.items():
            if key == stage_id:
                combo_table = f"combos_for_{value}"
                print(combo_table)
                break
                

        select_query = f'''
            INSERT INTO {combo_table} (
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
                lower_pre_game_id
            )
            SELECT 
                higher_port_player_post_frames.id AS higher_post_id, 
                higher_port_player_post_frames.frame AS higher_post_frame, 
                higher_port_player_post_frames.player_index AS higher_post_player_index,
                higher_port_player_post_frames.is_follower AS higher_post_is_follower,
                higher_port_player_post_frames.internal_character_id AS higher_post_internal_character_id,
                higher_port_player_post_frames.action_state_id AS higher_post_action_state_id,
                higher_port_player_post_frames.position_x AS higher_post_position_x,
                higher_port_player_post_frames.position_y AS higher_post_position_y,
                higher_port_player_post_frames.facing_direction AS higher_post_facing_direction,
                higher_port_player_post_frames.percent AS higher_post_percent,
                higher_port_player_post_frames.shield_size AS higher_post_shield_size,
                higher_port_player_post_frames.last_attack_landed AS higher_post_last_attack_landed,
                higher_port_player_post_frames.last_hit_by AS higher_post_last_hit_by,
                higher_port_player_post_frames.stocks_remaining AS higher_post_stocks_remaining,
                higher_port_player_post_frames.action_state_counter AS higher_post_action_state_counter,
                higher_port_player_post_frames.misc_action_state AS higher_post_misc_action_state,
                higher_port_player_post_frames.is_airborne AS higher_post_is_airborne,
                higher_port_player_post_frames.last_ground_id AS higher_post_last_ground_id,
                higher_port_player_post_frames.jumps_remaining AS higher_post_jumps_remaining,
                higher_port_player_post_frames.l_cancel_status AS higher_post_l_cancel_status,
                higher_port_player_post_frames.hurtbox_collision_state AS higher_post_hurtbox_collision_state,
                higher_port_player_post_frames.hitlag_remaining AS higher_post_hitlag_remaining,
                higher_port_player_post_frames.animation_index AS higher_post_animation_index,
                higher_port_player_post_frames.self_induced_speeds_air_x AS higher_post_self_induced_speeds_air_x,
                higher_port_player_post_frames.self_induced_speeds_y AS higher_post_self_induced_speeds_y,
                higher_port_player_post_frames.self_induced_speeds_attack_x AS higher_post_self_induced_speeds_attack_x,
                higher_port_player_post_frames.self_induced_speeds_attack_y AS higher_post_self_induced_speeds_attack_y,
                higher_port_player_post_frames.self_induced_speeds_ground_x AS higher_post_self_induced_speeds_ground_x,
                higher_port_player_post_frames.game_id AS higher_post_game_id,
                higher_port_player_pre_frames.id AS higher_pre_id,
                higher_port_player_pre_frames.frame AS higher_pre_frame,
                higher_port_player_pre_frames.player_index AS higher_pre_player_index,
                higher_port_player_pre_frames.is_follower AS higher_pre_is_follower,
                higher_port_player_pre_frames.seed AS higher_pre_seed,
                higher_port_player_pre_frames.action_state_id AS higher_pre_action_state_id,
                higher_port_player_pre_frames.position_x AS higher_pre_position_x,
                higher_port_player_pre_frames.position_y AS higher_pre_position_y,
                higher_port_player_pre_frames.facing_direction AS higher_pre_facing_direction,
                higher_port_player_pre_frames.joy_stick_x AS higher_pre_joy_stick_x,
                higher_port_player_pre_frames.joy_stick_y AS higher_pre_joy_stick_y,
                higher_port_player_pre_frames.c_stick_x AS higher_pre_c_stick_x,
                higher_port_player_pre_frames.c_stick_y AS higher_pre_c_stick_y,
                higher_port_player_pre_frames.trigger AS higher_pre_trigger,
                higher_port_player_pre_frames.buttons AS higher_pre_buttons,
                higher_port_player_pre_frames.physical_buttons AS higher_pre_physical_buttons,
                higher_port_player_pre_frames.physical_l_trigger AS higher_pre_physical_l_trigger,
                higher_port_player_pre_frames.physical_r_trigger AS higher_pre_physical_r_trigger,
                higher_port_player_pre_frames.raw_joy_stick_x AS higher_pre_raw_joy_stick_x,
                higher_port_player_pre_frames.percent AS higher_pre_percent,
                higher_port_player_pre_frames.game_id AS higher_pre_game_id,
                lower_port_player_post_frames.id AS lower_post_id,
                lower_port_player_post_frames.frame AS lower_post_frame,
                lower_port_player_post_frames.player_index AS lower_post_player_index,
                lower_port_player_post_frames.is_follower AS lower_post_is_follower,
                lower_port_player_post_frames.internal_character_id AS lower_post_internal_character_id,
                lower_port_player_post_frames.action_state_id AS lower_post_action_state_id,
                lower_port_player_post_frames.position_x AS lower_post_position_x,
                lower_port_player_post_frames.position_y AS lower_post_position_y,
                lower_port_player_post_frames.facing_direction AS lower_post_facing_direction,
                lower_port_player_post_frames.percent AS lower_post_percent,
                lower_port_player_post_frames.shield_size AS lower_post_shield_size,
                lower_port_player_post_frames.last_attack_landed AS lower_post_last_attack_landed,
                lower_port_player_post_frames.last_hit_by AS lower_post_last_hit_by,
                lower_port_player_post_frames.stocks_remaining AS lower_post_stocks_remaining,
                lower_port_player_post_frames.action_state_counter AS lower_post_action_state_counter,
                lower_port_player_post_frames.misc_action_state AS lower_post_misc_action_state,
                lower_port_player_post_frames.is_airborne AS lower_post_is_airborne,
                lower_port_player_post_frames.last_ground_id AS lower_post_last_ground_id,
                lower_port_player_post_frames.jumps_remaining AS lower_post_jumps_remaining,
                lower_port_player_post_frames.l_cancel_status AS lower_post_l_cancel_status,
                lower_port_player_post_frames.hurtbox_collision_state AS lower_post_hurtbox_collision_state,
                lower_port_player_post_frames.hitlag_remaining AS lower_post_hitlag_remaining,
                lower_port_player_post_frames.animation_index AS lower_post_animation_index,
                lower_port_player_post_frames.self_induced_speeds_air_x AS lower_post_self_induced_speeds_air_x,
                lower_port_player_post_frames.self_induced_speeds_y AS lower_post_self_induced_speeds_y,
                lower_port_player_post_frames.self_induced_speeds_attack_x AS lower_post_self_induced_speeds_attack_x,
                lower_port_player_post_frames.self_induced_speeds_attack_y AS lower_post_self_induced_speeds_attack_y,
                lower_port_player_post_frames.self_induced_speeds_ground_x AS lower_post_self_induced_speeds_ground_x,
                lower_port_player_post_frames.game_id AS lower_post_game_id,
                lower_port_player_pre_frames.id AS lower_pre_id,
                lower_port_player_pre_frames.frame AS lower_pre_frame,
                lower_port_player_pre_frames.player_index AS lower_pre_player_index,
                lower_port_player_pre_frames.is_follower AS lower_pre_is_follower,
                lower_port_player_pre_frames.seed AS lower_pre_seed,
                lower_port_player_pre_frames.action_state_id AS lower_pre_action_state_id,
                lower_port_player_pre_frames.position_x AS lower_pre_position_x,
                lower_port_player_pre_frames.position_y AS lower_pre_position_y,
                lower_port_player_pre_frames.facing_direction AS lower_pre_facing_direction,
                lower_port_player_pre_frames.joy_stick_x AS lower_pre_joy_stick_x,
                lower_port_player_pre_frames.joy_stick_y AS lower_pre_joy_stick_y,
                lower_port_player_pre_frames.c_stick_x AS lower_pre_c_stick_x,
                lower_port_player_pre_frames.c_stick_y AS lower_pre_c_stick_y,
                lower_port_player_pre_frames.trigger AS lower_pre_trigger,
                lower_port_player_pre_frames.buttons AS lower_pre_buttons,
                lower_port_player_pre_frames.physical_buttons AS lower_pre_physical_buttons,
                lower_port_player_pre_frames.physical_l_trigger AS lower_pre_physical_l_trigger,
                lower_port_player_pre_frames.physical_r_trigger AS lower_pre_physical_r_trigger,
                lower_port_player_pre_frames.raw_joy_stick_x AS lower_pre_raw_joy_stick_x,
                lower_port_player_pre_frames.percent AS lower_pre_percent,
                lower_port_player_pre_frames.game_id AS lower_pre_game_id
                FROM higher_port_player_post_frames
                LEFT JOIN higher_port_player_pre_frames ON higher_port_player_post_frames.frame = higher_port_player_pre_frames.frame AND higher_port_player_post_frames.game_id = higher_port_player_pre_frames.game_id
                LEFT JOIN lower_port_player_post_frames ON higher_port_player_post_frames.frame = lower_port_player_post_frames.frame AND higher_port_player_post_frames.game_id = lower_port_player_post_frames.game_id
                LEFT JOIN lower_port_player_pre_frames ON higher_port_player_post_frames.frame = lower_port_player_pre_frames.frame AND higher_port_player_post_frames.game_id = lower_port_player_pre_frames.game_id
                WHERE 
                higher_port_player_post_frames.game_id = %s
                AND (
                    higher_port_player_post_frames.action_state_id IN (0, 1, 2, 4, 8, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 181, 227, 228, 238, 239, 240, 241, 242)
                    OR higher_port_player_post_frames.hitlag_remaining > 0
                )
                OR (
                    lower_port_player_post_frames.game_id = %s
                    AND (
                        lower_port_player_post_frames.action_state_id IN (0, 1, 2, 4, 8, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 181, 227, 228, 238, 239, 240, 241, 242)
                        OR lower_port_player_post_frames.hitlag_remaining > 0
                    )
                )
        '''
        
        cursor.execute(select_query, (game_id, game_id))
        connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

move_combo_data_to_proper_stage()
