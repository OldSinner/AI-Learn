from game.base_snake import BaseSnake, get_direction_from_keyboard
from models.types import Vector
from config.game_config import CELL_GRID


class SnakeAI(BaseSnake):
    def get_reward(self, old_distance: int) -> float:
        reward = -0.05
        new_distance = self.get_distance_to_food()

        if new_distance < old_distance:
            reward += 0.5
        elif new_distance > old_distance:
            reward -= 0.25

        if self.snake[0] == self.food:
            return 10

        if (
            self.snake[0].x > CELL_GRID[0]
            or self.snake[0].x < 0
            or self.snake[0].y > CELL_GRID[1]
            or self.snake[0].y < 0
        ):
            return -10
        return reward

    def get_state(self) -> tuple:
        food_front = False
        food_left = False
        food_right = False

        if self.direction == Vector(1, 0):  # Moving RIGHT
            food_front = self.snake[0].x < self.food.x
            food_left = self.snake[0].y > self.food.y
            food_right = self.snake[0].y < self.food.y
        elif self.direction == Vector(-1, 0):  # Moving LEFT
            food_front = self.snake[0].x > self.food.x
            food_left = self.snake[0].y < self.food.y
            food_right = self.snake[0].y > self.food.y
        elif self.direction == Vector(0, 1):  # Moving DOWN
            food_front = self.snake[0].y < self.food.y
            food_left = self.snake[0].x < self.food.x
            food_right = self.snake[0].x > self.food.x
        elif self.direction == Vector(0, -1):  # Moving UP
            food_front = self.snake[0].y > self.food.y
            food_left = self.snake[0].x > self.food.x
            food_right = self.snake[0].x < self.food.x

        # Add distance information for better learning
        distance = self.get_distance_to_food()
        distance_level = min(distance // 5, 3)  # 0-3 levels

        return (food_front, food_left, food_right, distance_level)