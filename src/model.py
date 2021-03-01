import torch.nn as nn
import torch


class Model(nn.Module):
    def __init__(self, input_size, n_actions):
        super(Model, self).__init__()

        self.net = nn.Sequential(
            nn.Linear(input_size, 50),
            nn.ReLU(),
            nn.Linear(50, n_actions)

        )

        # self.net1 = nn.Sequential(
        #     nn.Linear(input_size, 50),
        #     nn.ReLU(),
        #     nn.Linear(50, 25),
        #     nn.ReLU(),
        #     nn.Linear(25, n_actions),
        # )

        self.apply(self._init_weights)

    def forward(self, x):
        """
        Assumes x is a tensor with the matrix raveled
        with torch.float format (see preprocess of PolicyAgent)
        """
        return self.net(x)

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
