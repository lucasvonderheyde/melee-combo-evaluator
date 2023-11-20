import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from sklearn.model_selection import train_test_split
import pandas as pd
import torch.optim as optim
import pdb
from constants import features, labels

def custom_loss(outputs, targets):

    mask = (targets != -999) & (targets != -1000)
    mse_loss = (outputs - targets) ** 2
    masked_loss = mse_loss * mask
    return masked_loss.mean()

csv_file_location = '../Jupyter/falco_vs_fox_csv_battlefield'

data = pd.read_csv(csv_file_location)
data.fillna(-999, inplace=True)

data = data.astype({col: 'int' for col in data.select_dtypes(['bool']).columns})

combo_features_and_labels = []

feature_index = features.index('character_creating_combo_for_model')

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
    features, all_labels = zip(*batch)
    features_padded = pad_sequence(features, batch_first=True, padding_value=-1000)

    # Extract the relevant label row (e.g., the last row) from each label tensor in the batch
    labels = torch.stack([label[-1] for label in all_labels], dim=0)

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
    def __init__(self, input_size=45, hidden_size=50, num_layers=2, output_size=6):
        super(BidirectionalComboLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_directions = 2  # Since it's bidirectional

        self.lstm = nn.LSTM(input_size=input_size,
                            hidden_size=hidden_size,
                            num_layers=num_layers,
                            batch_first=True,
                            bidirectional=True)
        
        self.fc = nn.Linear(hidden_size * self.num_directions, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers * self.num_directions, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers * self.num_directions, x.size(0), self.hidden_size).to(x.device)

        output, _ = self.lstm(x, (h0, c0))
        hidden = torch.cat((output[:, -1, :self.hidden_size], output[:, 0, self.hidden_size:]), dim=1)
        out = self.fc(hidden)
        return out

# Instantiate the model
model = BidirectionalComboLSTM()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)



model = BidirectionalComboLSTM(input_size=45, hidden_size=50, num_layers=2, output_size=6)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

test_batch = next(iter(train_loader))
print("Feature batch shape:", test_batch[0].shape)
print("Label batch shape:", test_batch[1].shape)

# Inside your training loop
num_epochs = 10  # Adjust as needed

num_epochs = 10  # Adjust as needed

num_epochs = 10  # Adjust as needed

for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for batch_features, batch_labels in train_loader:
        optimizer.zero_grad()

        outputs = model(batch_features)  # Forward pass

        character_mask = batch_features[:, :, feature_index]  # Use the correct index
        mask = torch.zeros_like(outputs)

        # Adjust the mask creation to match the output dimensions
        mask_higher_port = (character_mask[:, -1] == 1).unsqueeze(-1).expand(-1, 3)  # Last timestep, expand to 3 features
        mask_lower_port = (character_mask[:, -1] != 1).unsqueeze(-1).expand(-1, 3)  # Last timestep, expand to 3 features

        mask[:, :3] = mask_higher_port
        mask[:, 3:] = mask_lower_port

        masked_outputs = outputs * mask
        loss = custom_loss(masked_outputs, batch_labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    print(f'Epoch {epoch + 1}/{num_epochs}, Training Loss: {avg_loss:.4f}')

    # Validation
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for batch_features, batch_labels in val_loader:
            outputs = model(batch_features)

            character_mask = batch_features[:, :, feature_index]  # Use the correct index
            mask = torch.zeros_like(outputs)

            mask_higher_port = (character_mask[:, -1] == 1).unsqueeze(-1).expand(-1, 3)
            mask_lower_port = (character_mask[:, -1] != 1).unsqueeze(-1).expand(-1, 3)

            mask[:, :3] = mask_higher_port
            mask[:, 3:] = mask_lower_port

            masked_outputs = outputs * mask
            val_loss += custom_loss(masked_outputs, batch_labels).item()

        avg_val_loss = val_loss / len(val_loader)
        print(f'Validation Loss: {avg_val_loss:.4f}')

test_loss = 0.0
model.eval()
with torch.no_grad():
    for batch_features, batch_labels in test_loader:
        outputs = model(batch_features)

        character_mask = batch_features[:, :, feature_index]  # Use the correct index
        mask = torch.zeros_like(outputs)

        mask_higher_port = (character_mask[:, -1] == 1).unsqueeze(-1).expand(-1, 3)
        mask_lower_port = (character_mask[:, -1] != 1).unsqueeze(-1).expand(-1, 3)

        mask[:, :3] = mask_higher_port
        mask[:, 3:] = mask_lower_port

        masked_outputs = outputs * mask
        test_loss += custom_loss(masked_outputs, batch_labels).item()

    avg_test_loss = test_loss / len(test_loader)
    print(f'Test Loss: {avg_test_loss:.4f}')


torch.save(model.state_dict(), './model_weights.pth')

