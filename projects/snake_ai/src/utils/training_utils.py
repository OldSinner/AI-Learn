from collections import defaultdict
import pickle
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
from ..models.types import Action


def tuple_to_action(t) -> Action:
    return list(Action)[t]


def save_agent(agent, filename="q_table.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(dict(agent.Q_Table), f)


def load_agent(agent, filename="q_table.pkl"):
    import pickle

    with open(filename, "rb") as f:
        data = pickle.load(f)
        agent.Q_Table = defaultdict(lambda: np.zeros(3), data)


def live_plot(episode_rewards, episode_points=None):
    clear_output(wait=True)
    episodes = np.arange(1, len(episode_rewards) + 1)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(episodes, episode_rewards, label="Total reward")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Reward per Episode")
    plt.grid(True)
    plt.legend()

    if episode_points is not None:
        plt.subplot(1, 2, 2)
        plt.plot(episodes, episode_points, label="Points", color="orange")
        plt.xlabel("Episode")
        plt.ylabel("Points")
        plt.title("Points per Episode")
        plt.grid(True)
        plt.legend()

    plt.tight_layout()
    plt.show()