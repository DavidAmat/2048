import numpy as np
import copy
import random
import sys
from collections import defaultdict
import src.common.constants as c
from src.common.movements import Movements


class Env:

    def __init__(self, grid_size):
        """
        grid_size: size of the matrix
        """
        # Status
        self.game_stat = -2  # 0: playing, 1: win, -1: lost, -2: ready to start

        # Actions
        self.actions = {0: Movements.up,
                        1: Movements.down,
                        2: Movements.left,
                        3: Movements.right}

        # Log in a list all the matrices in each step
        self.log = defaultdict(list)

        # Initialize matrix
        self._init_matrix(grid_size)

        # Score accumulated
        self.game_score = 0

    def _init_matrix(self, n):
        """
        Initializes the game matrix
        """
        self.matrix = np.zeros((n, n))
        self._add_two(times=2)

        # Log
        self.log["mat"].append(self.matrix)
        self.log["action"].append(-1)  # randomly added action
        self.log["reward"].append(0)

    def _add_two(self, times, choices=c.RANDOM_NUMBER_CHOICES, probs_choices=c.PROBAB_NUMBER_CHOICES):
        """
        Add to the matrix randomly a 2 and 4
        """
        for _ in range(times):
            # choose only cells with a 0
            avail_cells = list(zip(*np.where(self.matrix == 0)))

            # Choose the new index of the matrix
            index_sample = random.sample(avail_cells, 1)[0]

            # Start the game always with a 2
            if self.game_stat == -2:
                self.matrix[index_sample] = 2

                # Change the stat to playing
                self.game_stat = 0

            elif len(avail_cells):
                #  Choose randomly between a 2 or a 4 and put it in the matrix
                value_sample = np.random.choice(choices, p=probs_choices)
                self.matrix[index_sample] = value_sample
            else:
                sys.exit("Finished game!")

    def _check_possible_action(self):
        """
         # Check if there is any possible action to take
         without modifying the env matrix
        """
        any_action_available = False
        test_matrix = copy.copy(self.matrix)
        for a_id in self.actions:
            _, action_available, _, _ = self.actions[a_id](test_matrix, 0)
            any_action_available |= action_available
        return any_action_available

    def _game_stat(self):
        """
        Status of the game:
        1: game won
        -1: game lost
        0: game in play
        """
        if self.matrix.min() == 0:
            if self.matrix.max() >= c.OBJECTIVE:
                self.game_stat = 1
            else:
                self.game_stat = 0
        else:
            if self._check_possible_action():
                self.game_stat = 0
            else:
                self.game_stat = -1

    # Play step
    def step(self, action_id):
        """
        Returns:
        - start matrix
        - final matrix
        - has_moved: if the action taken has lead to a movement (True) or not (False)
        - reward
        - game stat
        """

        # Take the action
        start_matrix = copy.copy(self.matrix)
        self.matrix, done, num_merges, added_merge = self.actions[action_id](self.matrix)

        #########################
        #      REWARD
        #########################
        # New definition of reward counting merges and number of 0
        collapsed_cells = np.log2(added_merge)
        penalty_cell_move = c.GRID_LEN**2 - np.sum(self.matrix == start_matrix)
        penalty_impossible_move = 99 if not done else 0
        reward = collapsed_cells - penalty_cell_move - penalty_impossible_move

        self.game_score += added_merge

        # Log
        self.log["mat"].append(self.matrix)
        self.log["action"].append(action_id)
        self.log["reward"].append(reward)

        # If the movement could be done
        if done:
            # Add randomly the next number in the matrix
            self._add_two(times=1)

            # Log
            self.log["mat"].append(self.matrix)
            self.log["action"].append(-1)  # action -1 is a randomly added number
            self.log["reward"].append(0)

            # Check game status if a further action is possible
            self._game_stat()

        # If the movement performed didn't change anything keep playing
        return start_matrix, self.matrix, done, reward, self.game_stat

    # Reset
    def reset(self):
        self.__init__(self.matrix.shape[0])
