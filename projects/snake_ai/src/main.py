from agents.snake_ai import SnakeAI
from game.base_snake import get_direction_from_keyboard

snake = SnakeAI()
import pygame

try:
    while snake.running:
        print("a")
        action = get_direction_from_keyboard()
        _, _, done = snake.step(action)
        if done:
            snake.reset()
        if not snake.running:
            pygame.quit()
finally:
    pygame.quit()