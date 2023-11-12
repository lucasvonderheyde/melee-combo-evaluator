import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from sklearn.model_selection import train_test_split
import pandas as pd


data = pd.read_csv('../Jupyter/falco_vs_fox_csv_battlefield')
data.fillna(-999, inplace=True)

data = data.astype({col: 'int' for col in data.select_dtypes(['bool']).columns})


features = [
    'higher_post_frame', 'higher_post_internal_character_id', 'higher_post_action_state_id', 'higher_post_position_x', 'higher_post_position_y', 'higher_post_facing_direction',
    'higher_post_percent', 'higher_post_action_state_counter', 'higher_post_misc_action_state','higher_post_last_ground_id', 'higher_post_jumps_remaining',
    'higher_post_l_cancel_status', 'higher_post_hitlag_remaining', 'higher_post_animation_index', 'higher_post_self_induced_speeds_air_x', 'higher_post_self_induced_speeds_y', 'higher_post_self_induced_speeds_attack_x',
    'higher_post_self_induced_speeds_attack_y', 'higher_post_self_induced_speeds_ground_x', 
    'lower_post_frame', 'lower_post_internal_character_id', 'lower_post_action_state_id', 'lower_post_position_x', 'lower_post_position_y', 'lower_post_facing_direction',
    'lower_post_percent', 'lower_post_action_state_counter', 'lower_post_misc_action_state', 'lower_post_is_airborne', 'lower_post_last_ground_id', 'lower_post_jumps_remaining',
    'lower_post_l_cancel_status', 'lower_post_hitlag_remaining', 'lower_post_animation_index', 'lower_post_self_induced_speeds_air_x', 'lower_post_self_induced_speeds_y', 'lower_post_self_induced_speeds_attack_x',
    'lower_post_self_induced_speeds_attack_y', 'lower_post_self_induced_speeds_ground_x', 
    'combo_block_for_model', 'character_creating_combo_for_model', 'attack_state_to_hit_in_combo_for_model', 'higher_port_damage_done_with_combo', 'lower_port_damage_done_with_combo'
]

labels = [
    'lower_port_l_cancel_for_model', 'higher_port_l_cancel_for_model', 'lower_port_damage_done_with_combo_model_score', 'higher_port_damage_done_with_combo_model_score', 'higher_port_x_position_model_score', 'higher_port_y_position_model_score',
    'lower_port_x_position_model_score', 'lower_port_y_position_model_score'
]

combo_features_and_labels = []


for combo_block, combo_data in data.groupby('combo_block_for_model'):
    
    combo_features = combo_data[features].apply(pd.to_numeric, errors='coerce').fillna(-999).values
    combo_labels = combo_data[labels].apply(pd.to_numeric, errors='coerce').fillna(-999).values

    if np.isnan(combo_features).any() or np.isinf(combo_features).any():
        raise ValueError("combo_features contains NaN or Inf.")
    if np.isnan(combo_labels).any() or np.isinf(combo_labels).any():
        raise ValueError("combo_labels contains NaN or Inf.")

    combo_features_tensor = torch.tensor(combo_features, dtype=torch.float32)
    combo_labels_tensor = torch.tensor(combo_labels, dtype=torch.float32)

    combo_features_and_labels.append((combo_block, combo_features_tensor, combo_labels_tensor))

class ComboDataset(Dataset):
    def __init__(self, features_and_labels):
        self.features_and_labels = features_and_labels

    def __len__(self):
        return len(self.features_and_labels)

    def __getitem__(self, idx):
        return self.features_and_labels[idx]
    
print(combo_features_and_labels[55])
    
debug_dataset = ComboDataset(combo_features_and_labels)
print(debug_dataset[0]) 
 