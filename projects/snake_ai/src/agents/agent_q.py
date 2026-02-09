from collections import defaultdict
import random

import numpy as np

from game.base_snake import BaseSnake
from utils.training_utils import tuple_to_action


class AgentQ:
    def __init__(self, game: BaseSnake) -> None:
        self.Q_Table = defaultdict(lambda: np.zeros(game.n_actions))
        self.alpha = 0.1  # Lower learning rate for stability
        self.gamma = 0.95  # Higher discount factor
        self.epsilon: float = 1
        self.game = game

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.game.n_actions - 1)
        else:
            return np.argmax(self.Q_Table[state])

    def make_step(self):
        old_state = tuple(self.game.get_state())
        action = self.get_action(old_state)
        new_state, reward, done = self.game.step(tuple_to_action(action))
        current_q = self.Q_Table[old_state][action]
        max_future_q = 0 if done else np.max(self.Q_Table[new_state])
        self.Q_Table[old_state][action] = self.calculate_q(
            current_q, max_future_q, reward
        )
        return new_state, reward, done

    def calculate_q(self, current_q, max_future_q, reward):
        return current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
