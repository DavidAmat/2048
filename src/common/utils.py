import numpy as np

class QValueCalc:
    def __init__(self):
        pass
    
    def __call__(self, rew, win = 10):
        """
        Lineal gamma discount on future state rewards
        """
        win = int(win)
        if not isinstance(rew, np.ndarray):
            rew = np.array(rew)
        gamma_vec = np.array([(win - idx)  / win for idx in range(win)])
        result = []
        for idx in range(rew.shape[0]):
            rew_win = rew[idx:idx+win]
            result.append(np.round(np.sum(rew_win*gamma_vec[:rew_win.shape[0]]),3))
        return result

    def old(self, rewards, gamma):
        """
        Calculates the discounted total reward for every step
        rewards: list of rewards for the whole episodes
        """
        res = []
        sum_r = 0.0

        # Calculate first the reward from the end of the local reward list
        for r in reversed(rewards):
            # The more far apart we are from the last step reward, the more discounted the reward
            sum_r *= gamma

            # local reward at that timestep
            sum_r += r
            res.append(sum_r)

        # reverse again the resulting q-vals list
        return list(reversed(res))
