import random
from collections import defaultdict
from typing import DefaultDict

import numpy as np

from game.base_snake import BaseSnake
from models.types import State
from utils.training_utils import tuple_to_action


class AgentQ:
    """Tabular Q-learning agent for .
    Notes
    - The Q-table maps environment states (tuples) to a vector of action values.
    - The environment exposes `n_actions` discrete actions and `step()` accepts an
      `Action` enum; `tuple_to_action()` converts our integer action index.
    """

    def __init__(
        self,
        game: BaseSnake,
        *,
        alpha: float = 0.1,
        gamma: float = 0.95,
        epsilon: float = 1.0,
    ) -> None:
        """Create a new Q-learning agent.

        Parameters
        - game: Snake environment instance.
        - alpha: Learning rate.
        - gamma: Discount factor.
        - epsilon: Exploration probability for epsilon-greedy action selection.
        """

        self.game = game
        self.alpha = float(alpha)
        self.gamma = float(gamma)
        self.epsilon = float(epsilon)

        self._q_table: DefaultDict[State, np.ndarray] = defaultdict(
            lambda: np.zeros(self.game.n_actions, dtype=np.float32)
        )

    @property
    def Q_Table(self) -> DefaultDict[State, np.ndarray]:
        """Backward-compatible access to the Q-table."""

        return self._q_table

    @Q_Table.setter
    def Q_Table(self, value: DefaultDict[State, np.ndarray]) -> None:
        """Backward-compatible setter used by `load_agent()`."""

        self._q_table = value

    def describe(self) -> str:
        """Return a short, human-readable agent configuration string."""

        return (
            "AgentQ("
            f"alpha={self.alpha:.4f}, gamma={self.gamma:.4f}, epsilon={self.epsilon:.4f}, "
            f"states={len(self._q_table)}"
            ")"
        )

    def get_action(self, state: State) -> int:
        """Choose an action index using epsilon-greedy selection."""

        if random.random() < self.epsilon:
            return random.randrange(self.game.n_actions)
        return int(np.argmax(self._q_table[state]))

    def make_step(self) -> tuple[State, float, bool]:
        """Run one environment step and update the Q-table."""

        old_state: State = tuple(self.game.get_state())
        action_idx = self.get_action(old_state)

        new_state, reward, done = self.game.step(tuple_to_action(action_idx))
        self.update(old_state, action_idx, new_state, reward, done)
        return new_state, float(reward), bool(done)

    def update(
        self,
        old_state: State,
        action_idx: int,
        new_state: State,
        reward: float,
        done: bool,
    ) -> None:
        """Apply the Q-learning update rule for a single transition."""
        current_q = float(self._q_table[old_state][action_idx])
        max_future_q = 0.0 if done else float(np.max(self._q_table[new_state]))

        self._q_table[old_state][action_idx] = self.calculate_q(
            current_q=current_q,
            max_future_q=max_future_q,
            reward=float(reward),
        )

    def calculate_q(
        self, *, current_q: float, max_future_q: float, reward: float
    ) -> float:
        """Compute the updated Q-value for the current state-action pair."""

        td_target = reward + self.gamma * max_future_q
        return current_q + self.alpha * (td_target - current_q)
