from collections import defaultdict
import numpy as np


class Player:
    """
    Debugging class for a random Player without policy
    """
    def __init__(self, env):
        self.env = env
        self.steps = 0
        self.game_stat = 0
        self.log = defaultdict(list)

    def play_random(self):
        while self.game_stat == 0:
            self.steps += 1

            # action random
            action_pl = np.random.choice(list(self.env.actions.keys()))

            # choose a random action
            start_matrix, end_matrix, done, reward, self.game_stat = self.env.step(action_pl)

            # log
            self.log["mat_o"].append(start_matrix)
            self.log["action"].append(action_pl)
            self.log["reward"].append(reward)
            self.log["mat_f"].append(end_matrix)
            self.log["done"].append(done)
            self.log["game_stat"].append(self.game_stat)
