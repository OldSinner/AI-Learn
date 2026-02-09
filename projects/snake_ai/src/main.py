from game.base_snake import get_direction_from_keyboard, BaseSnake


snake = BaseSnake()
import pygame

try:
    while snake.running:
        action = get_direction_from_keyboard()
        _, _, done = snake.step(action)
        if done:
            snake.reset()
        if not snake.running:
            pygame.quit()
finally:
    pygame.quit()


# def train_agent(agent : AgentQ, num_episodes=10000, epsilon_decay=0.9995, min_epsilon=0.01):
#     episode_rewards = []
#     episode_points = []
#     avg_rewards = []
#     avg_points = []
#     for episode in range(num_episodes):
#         agent.game.reset()
#         done = False
#         total_reward = 0
#         steps = 0
#         if not agent.game.running:
#             break
#         while not done and steps < 500:  # Limit steps to prevent infinite episodes
#             _, reward, done = agent.make_step()
#             total_reward += reward
#             steps += 1
#         episode_rewards.append(total_reward)
#         episode_points.append(agent.game.points)
#         agent.epsilon = max(min_epsilon, agent.epsilon * epsilon_decay)
#         if episode % 50 == 0:
#             avg_reward = statistics.mean(episode_rewards)
#             avg_point = statistics.mean(episode_points)
#             avg_rewards.append(avg_reward)
#             avg_points.append(avg_point)
#             episode_rewards = []
#             episode_points = []
#             live_plot(avg_rewards, avg_points)
#             print(f"Episode {episode}/{num_episodes}, Epsilon: {agent.epsilon:.4f}, Avg Reward: {np.mean(episode_rewards[-100:]):.3f}")
#         if episode % 100 == 0:
#             save_agent(agent, f"q_table_{episode}.pkl")
#     plt.ioff()
#     plt.show()
# try:
#     game = Game()
#     # agent = AgentQ(game)

#     while True:
#         game.step_with_keyboard()

#     # train_agent(agent)
# finally:
#     pygame.quit()
# def randomAction() -> tuple[int, int, int]:
#     index = random.randint(0, 2)
#     return (1 if index == 0 else 0, 1 if index == 1 else 0, 1 if index == 2 else 0)
