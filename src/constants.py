internal_character_ids = {
    0: "Mario",
    1: "Fox",
    7: "Shiek",
    18: "Marth",
    19: "Zelda",
    22: "Falco"
}

stage_ids ={
    31: "Battlefield"
}

features = [
    'higher_post_frame', 'higher_post_internal_character_id', 'higher_post_action_state_id',
    'higher_post_position_x', 'higher_post_position_y', 'higher_post_facing_direction',
    'higher_post_percent', 'higher_post_action_state_counter', 'higher_post_misc_action_state',
    'higher_post_last_ground_id', 'higher_post_jumps_remaining','higher_post_l_cancel_status', 
    'higher_post_hitlag_remaining', 'higher_post_animation_index', 'higher_post_self_induced_speeds_air_x', 
    'higher_post_self_induced_speeds_y', 'higher_post_self_induced_speeds_attack_x', 'higher_post_self_induced_speeds_attack_y', 
    'higher_post_self_induced_speeds_ground_x',  
    'lower_post_frame', 'lower_post_internal_character_id', 'lower_post_action_state_id', 
    'lower_post_position_x', 'lower_post_position_y', 'lower_post_facing_direction',
    'lower_post_percent', 'lower_post_action_state_counter', 'lower_post_misc_action_state', 
    'lower_post_last_ground_id', 'lower_post_jumps_remaining',
    'lower_post_l_cancel_status', 'lower_post_hitlag_remaining', 'lower_post_animation_index', 
    'lower_post_self_induced_speeds_air_x', 'lower_post_self_induced_speeds_y', 'lower_post_self_induced_speeds_attack_x',
    'lower_post_self_induced_speeds_attack_y', 'lower_post_self_induced_speeds_ground_x', 
    'combo_block_for_model', 'attack_state_to_hit_in_combo_for_model', 'character_creating_combo_for_model', 'lower_port_l_cancel_for_model',
    'higher_port_l_cancel_for_model', 'lower_port_damage_done_with_combo', 'higher_port_damage_done_with_combo'
]

labels = [
    'lower_port_damage_done_with_combo_model_score', 'higher_port_damage_done_with_combo_model_score', 'higher_port_x_position_model_score', 
    'higher_port_y_position_model_score','lower_port_x_position_model_score', 'lower_port_y_position_model_score'
]