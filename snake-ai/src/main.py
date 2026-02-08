from snakenotail import SnakeAI
from basesnake import get_direction_from_keyboard

snake = SnakeAI()
import pygame

try:
    while snake.running:
        action = get_direction_from_keyboard()
        _, _, done = snake.step(action)
        if done:
            print("ugabuga")
            snake.game_reset()
        if not snake.running:
            pygame.quit()
finally:
    pygame.quit()
