import numpy as np
import torch
import torch.nn.functional as F
import src.common.constants as c

class PolicyAgent:
    """
    Policy agent gets action probabilities from the model and samples actions from it
    :params num_actions: number of actions to choose from the environment
    :params model: instance of the PyTorch model (network)
    :params state_repr: represent states by "log2" of the matrix or "bin" matrices
    """

    # TODO: unify code with DQNAgent, as only action selector is differs.
    def __init__(self, model, num_actions, state_repr="log2", device="cpu"):
        self.model = model
        self.device = device
        self.num_actions = num_actions
        self.state_repr = state_repr

    def _convert_log2(self, state):
        """
        Converts the game matrix to a log2, replacing log2(0) by a 0
        since no 1 is present in the matrix never
        """
        state = np.log2(state)
        state[state == -np.inf] = 0
        return state

    def _to_binary(self, state, positions=c.BINARY_POSITIONS):
        """
        Returns the binary representation of {0,1}^16
        of the matrix (each cell is converted to a
        binary vector representing its binary number)
        """
        states_flat = state.ravel().astype(int)
        return (((states_flat[:, None] & (1 << np.arange(positions)))) > 0).astype(int)

    def preprocess(self, state):
        """
        Given the game matrix (state) returns different
        representations of such matrix to be input of
        the neural network
        """
        if self.state_repr == "log2":
            state = self._convert_log2(state)
            return torch.tensor(state.ravel(), dtype=torch.float)
        elif self.state_repr == "bin":
            state = self._to_binary(state)
            return torch.tensor(state, dtype=torch.float).view(-1)

    @torch.no_grad()
    def get_action_probs(self, state):
        """
        Given a state matrix, get the probs of the last layer
        """
        state = self.preprocess(state).unsqueeze(0).to(self.device)
        return self.get_action_probs_batch(state)
    
    @torch.no_grad()
    def get_action_probs_batch(self, tensor_states):
        """
        Receives a batch of N states of length S (N x S)
        and forwards them into the model
        """
        return F.softmax(self.model(tensor_states), dim=1).data.cpu().numpy()
    
    @torch.no_grad()
    def __call__(self, state, epsilon=0):
        """
        Return actions from given a state
        :param state: matrix of state
        :param epsilon: epsilon value to choose from random action
        :return: action index
        """
        assert isinstance(state, np.ndarray)
        # take a random choice
        if (epsilon > 0) & (np.random.rand() < epsilon):
            return np.random.choice(self.num_actions)

        # forward the state to get the actions probabilities
        else:
            probs = self.get_action_probs(state).ravel()
            return np.random.choice(self.num_actions, p=probs)
