
import torch
import torch.nn as nn

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
