import numpy as np
import warnings
import torch
import time
import torch.optim as optim
import torch.nn.functional as F
from tensorboardX import SummaryWriter

import src.common.constants as c
from src.env import Env
from src.model import Model
from src.agent import PolicyAgent
from src.epsilon import EpsilonPolicy
from src.experience import ExperienceSource
from src.common.utils import QValueCalc

warnings.filterwarnings("ignore")

# Game initialize
env = Env(c.GRID_LEN)
eps = EpsilonPolicy(eps_start=0.8, eps_decay=200, eps_final=0.01)
input_size = c.BINARY_POSITIONS * c.GRID_LEN**2 if c.STATE_REPR == "bin" else c.GRID_LEN**2
model = Model(input_size, len(env.actions))
agent = PolicyAgent(model=model, num_actions=len(env.actions), state_repr=c.STATE_REPR)
exp = ExperienceSource(env, agent, eps)
qv = QValueCalc()

# Training
version = "REINF-v1-log2"
writer = SummaryWriter(comment=f"-2048-{version}", log_dir=f"runs/{version}")
# optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
optimizer = optim.RMSprop(model.parameters(), lr=c.LEARNING_RATE, alpha=0.99)

# Log
game_scores = []  # scores for each episode
steps_reach = []  # steps reached for each episode
game_wins = []  # whether 0: game lost, 1: game won

# Counters
step_idx = 0
done_episodes = 0
epoch_idx = 0
mean_wins = 0

################
#   Epochs
################

while epoch_idx < c.EPOCHS:

    # Control
    start_time = time.time()

    # For each step in the episode, keep track also of states, actions, rewards -> qvals
    batch_states, batch_actions, batch_rewards, batch_transf_states = [], [], [], []

    ###############
    # Batchs
    ###############
    # Play several games with the same policy
    batch_episodes = 0

    # For each batch
    for batch_id in range(c.BATCHS):

        # Generate a episode
        exp.populate_episode(epoch_idx)

        # Iterate through episode
        for idx, exp_step in enumerate(exp.history):

            # Ignore unfeasible moves
            if not exp_step.done:
                continue

            # Fill with experience data
            batch_states.append(exp_step.state)
            batch_transf_states.append(agent.preprocess(exp_step.state).data.numpy())  # save as numpy the transformed game matrix
            batch_actions.append(int(exp_step.action))
            batch_rewards.append(exp_step.reward)

        # standarize and convert rewards to q values according to REINFORCE
        st_rew = np.round((np.array(batch_rewards) - np.mean(batch_rewards)) / (np.std(batch_rewards)), 3)
        batch_qvals = qv(st_rew, c.GAMMA)

        # Get last step number
        steps = len(exp.history)
        steps_reach.append(steps)

        # Get the final score in the episode
        game_score_final = exp.env.game_score
        game_scores.append(game_score_final)

        # Get if the game was won (1) or not (0)
        game_stat_final = 0 if exp.env.game_stat == -1 else 1
        game_wins.append(game_stat_final)

        # Reset the board to play another episode
        # inside this batch (we play BATCHS episodes in this batch)
        exp.reset()

        # Inform Tensorboard
    mean_game_scores = float(np.mean(game_scores[-c.BATCHS:]))
    mean_wins = np.round(float(np.mean(game_wins[-c.BATCHS:])) ,3)
    mean_steps = np.round(float(np.mean(steps_reach[-c.BATCHS:])) ,3)
    writer.add_scalar("mean_game_scores", mean_game_scores, epoch_idx)
    writer.add_scalar("mean_wins", mean_wins, epoch_idx)
    writer.add_scalar("mean_steps", mean_steps, epoch_idx)

    # When the problem is solved stop training
    if (mean_wins > c.GAME_WIN_RATE) & (epoch_idx > 20):
        break

    ##############################
    # Training neural network
    ##############################
    optimizer.zero_grad()

    # Converting to tensors the matrices of each observation in the episode
    # ----------------------------------------------------------------------

    # shape: [# steps, c.GRID_LEN, c.GRID_LEN]
    tensor_states = torch.FloatTensor(batch_states)

    # shape [# steps]
    tensor_actions = torch.LongTensor(batch_actions)
    tensor_qvals = torch.FloatTensor(batch_qvals)

    # Forward to the network to get logits
    # we will forward tensor states with the following shape
    # [#steps, c.GRID_LEN * c.GRID_LEN]
    logits = model(tensor_states.view(-1, input_size))

    # Convert logits to log_softmax
    log_softmax = F.log_softmax(logits, dim=1)

    # From the probabilities got, mask with the actions taken
    # log_softmax is [#steps in game, 4 (actions)] so we will
    # convert it to [# steps, 1 (action taken)]
    log_softmax_action = log_softmax.gather(1, tensor_actions.unsqueeze(1)).squeeze(1)

    # The loss will be the weighted sum over steps in the episode
    # of the Q values (tensor_qvals) weighting the log(policy(s,a))
    # which is the log_softmax_action
    loss = -tensor_qvals * log_softmax_action
    loss_mean = loss.mean()
    writer.add_scalar("loss", np.round(loss_mean.item(), 4), epoch_idx)

    # Backpropagate
    loss_mean.backward()
    optimizer.step()

    # Control
    end_time = time.time()

    if ((epoch_idx % 1) == 0) & (epoch_idx > 0):
        print("Epoch: ", epoch_idx,
              ", Game_scores_mean: ", mean_game_scores,
              ", Mean reward: ", np.round(np.mean(batch_rewards), 2),
              ", Mean wins: ", mean_wins,
              ", Mean steps: ", mean_steps,
              ", Exec time epoch: ", round(end_time-start_time, 2),
              ", Epsilon: ", np.round(eps.get_epsilon(epoch_idx),3)
              )

    # Reset the experience source and add epoch counter
    exp.reset()
    epoch_idx += 1

writer.close()