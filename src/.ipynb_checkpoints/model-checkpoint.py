import torch.nn as nn
import torch


class Model(nn.Module):
    def __init__(self, input_size, n_actions):
        super(Model, self).__init__()
        
        fc1_units = 64
        fc2_units = 64
        fc3_units = 64
        
        self.seed = torch.manual_seed(32)
        
        self.fc1 = nn.Linear(input_size, fc1_units)
        self.bn1 = nn.BatchNorm1d(fc1_units)
        self.act1 = nn.ReLU()
        self.fc2 = nn.Linear(fc1_units, fc2_units)
        self.bn2 = nn.BatchNorm1d(fc2_units)
        self.act2 = nn.ReLU()
        self.fc3 = nn.Linear(fc2_units, fc3_units)
        self.bn3 = nn.BatchNorm1d(fc3_units)
        self.act3 = nn.ReLU()
        self.fc4 = nn.Linear(fc3_units, n_actions)

        #self.apply(self._init_weights)

    def forward(self, state):
        """
        Assumes state is a tensor with the matrix raveled
        with torch.float format (see preprocess of PolicyAgent)
        """
        x = self.fc1(state)
        x = self.act1(x)
        #x = self.bn1(x)
        x = self.fc2(x)
        x = self.act2(x)
        #x = self.bn2(x)
        x = self.fc3(x)
        x = self.act3(x)
        return self.fc4(x)

    def _init_weights(self, m):
        """
        Initializes all weights and biases to the same quantity
        to avoid initially getting stucked into a action value
        when the network is just exploring and taking the same step
        which may lead the matrix in the same corner without moving
        until another action is sampled.
        """
        if type(m) == nn.Linear:
            torch.nn.init.xavier_uniform_(m.weight)
            # m.bias.data.fill_(0.01)
