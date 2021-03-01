
class EpsilonPolicy:
    """
    Sets a decayment policy of the epsilon for the
    agent to ignore the policy-based action
    and perform a random action instead when training
    First epochs should have higher epsilon to allow exploration
    :params eps_decay: number of epochs in which epsilon goes from eps_start to eps_decay
    """

    def __init__(self, eps_start, eps_decay, eps_final):
        self.eps_start = eps_start
        self.eps_final = eps_final
        self.eps_decay = eps_decay

    def get_epsilon(self, epoch):
        return max(self.eps_final, self.eps_start - epoch / self.eps_decay)
