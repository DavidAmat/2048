from collections import namedtuple

ExperienceEpisode = namedtuple('ExperienceEpisode', ('state', 'action', 'done', 'reward',  'game_stat', 'epsilon'))


class ExperienceSource:
    """
    Helps in the REINFORCE algorithm providing
    - A continuous source of steps for 1 single episode until the buffer gets reset
    - Inputs:
        - env:
        - agent: performs actions based on a policy (REINFORCE -> on-policy)
        - epsilon_policy: instance of class EpsilonPolicy
    Returns:
        - reward: for each step
        - state: state for each step in the episode
        - action: action decided by the agent to be taken at each step

    """
    def __init__(self, env, agent, epsilon_policy):
        self.env = env
        self.agent = agent
        self.epsilon_policy = epsilon_policy

        # Attributes
        self.history = []  # history of ExperienceSource instances for 1 entire episode
        self.steps = 0  # counter of actions performed
        self.epsilon = epsilon_policy.get_epsilon(0)  # starting epsilon at epoch = 0
        self.env.reset()  # Reset env

    def populate_episode(self, epoch_num):

        # Play until the episode finishes
        game_stat = 0

        while game_stat == 0:

            # Count steps
            self.steps += 1

            # use the agent's policy to choose next action and also input the epsilon policy
            self.epsilon = self.epsilon_policy.get_epsilon(epoch_num)
            action_id = self.agent(self.env.matrix, self.epsilon)

            # Take the choosen action
            start_matrix, end_matrix, done, reward, game_stat = self.env.step(action_id)

            # fill the history of steps
            self.history.append(ExperienceEpisode(state=start_matrix, action=action_id,
                                                  done=done, reward=reward,
                                                  game_stat=game_stat, epsilon=self.epsilon))



    def reset(self):
        self.history = []
        self.steps = 0
        self.epsilon = self.epsilon_policy.get_epsilon(0)
        self.env.reset()
