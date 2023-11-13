import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from sklearn.model_selection import train_test_split
import pandas as pd
import torch.optim as optim

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
    'combo_block_for_model', 'character_creating_combo_for_model', 'attack_state_to_hit_in_combo_for_model', 'higher_port_damage_done_with_combo', 'lower_port_damage_done_with_combo', 'lower_port_l_cancel_for_model', 'higher_port_l_cancel_for_model'
]

labels = [
    'lower_port_damage_done_with_combo_model_score', 'higher_port_damage_done_with_combo_model_score', 'higher_port_x_position_model_score', 'higher_port_y_position_model_score',
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
        combo_block, features_tensor, labels_tensor = self.features_and_labels[idx]
        return features_tensor, labels_tensor
    
def collate_fn(batch):
    # Separate features and labels
    features, labels = zip(*batch)
    # Pad features
    features_padded = pad_sequence(features, batch_first=True, padding_value=-1000)
    # Directly use labels (already tensors)
    return features_padded, labels

# Instantiate ComboDataset with your data
combo_training_data_set = ComboDataset(combo_features_and_labels)

# Example of using DataLoader with your dataset and custom collate function
data_loader = DataLoader(combo_training_data_set, batch_size=32, collate_fn=collate_fn)

# Splitting combo_features_and_labels into train, validation, and test sets
train_features_and_labels, test_features_and_labels = train_test_split(combo_features_and_labels, test_size=0.3, random_state=42)
val_features_and_labels, test_features_and_labels = train_test_split(test_features_and_labels, test_size=0.5, random_state=42)

# Creating datasets
train_dataset = ComboDataset(train_features_and_labels)
val_dataset = ComboDataset(val_features_and_labels)
test_dataset = ComboDataset(test_features_and_labels)

# Creating DataLoaders
train_loader = DataLoader(train_dataset, batch_size=32, collate_fn=collate_fn)
val_loader = DataLoader(val_dataset, batch_size=32, collate_fn=collate_fn)
test_loader = DataLoader(test_dataset, batch_size=32, collate_fn=collate_fn)


class BidirectionalComboLSTM(nn.Module):
    def __init__(self, input_size=46, hidden_size=50, num_layers=2, output_size=3):
        super(BidirectionalComboLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_directions = 2  # Since it's bidirectional

        self.lstm = nn.LSTM(input_size=input_size,
                            hidden_size=hidden_size,
                            num_layers=num_layers,
                            batch_first=True,
                            bidirectional=True)
        
        # Doubling the output features because of bidirectionality
        self.fc = nn.Linear(hidden_size * self.num_directions, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers * self.num_directions, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers * self.num_directions, x.size(0), self.hidden_size).to(x.device)

        output, (hn, cn) = self.lstm(x, (h0, c0))
        # Concatenate the final forward and backward hidden state
        hidden = torch.cat((hn[-2,:,:], hn[-1,:,:]), dim=1)
        out = self.fc(hidden)


model = BidirectionalComboLSTM(input_size=46, hidden_size=50, num_layers=2, output_size=3)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10  # This is a hyperparameter you can tune

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for batch_features, batch_labels in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_features)
        loss = criterion(outputs, batch_labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader)}")

    # Validation step
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for batch_features, batch_labels in val_loader:
            outputs = model(batch_features)
            loss = criterion(outputs, batch_labels)
            val_loss += loss.item()
    print(f"Validation Loss: {val_loss/len(val_loader)}")

    test_loss = 0.0
model.eval()
with torch.no_grad():
    for batch_features, batch_labels in test_loader:
        outputs = model(batch_features)
        loss = criterion(outputs, batch_labels)
        test_loss += loss.item()
print(f"Test Loss: {test_loss/len(test_loader)}")