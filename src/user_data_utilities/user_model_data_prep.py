import numpy as np
import pandas as pd
import torch

def prep_user_model_data(combo_data, features):

    user_combo_data = pd.read_csv(combo_data)
    user_combo_data.fillna(-999, inplace=True)

    user_combo_data = user_combo_data.astype({col: 'int' for col in user_combo_data.select_dtypes(['bool']).columns})

    combo_features = user_combo_data[features].apply(pd.to_numeric, errors='coerce').fillna(-999).values

    if np.isnan(combo_features).any() or np.isinf(combo_features).any():
        raise ValueError("combo_features contains NaN or Inf.")

    combo_features_tensor = torch.tensor(combo_features, dtype=torch.float32)

    print("Shape before unsqueeze:", combo_features_tensor.shape)

    combo_features_tensor = combo_features_tensor.unsqueeze(0) 

    return combo_features_tensor