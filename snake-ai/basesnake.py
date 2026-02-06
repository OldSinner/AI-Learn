from collections import deque
import random
from model import Vector, Action
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
FPS = 360
SNAKE = (0, 255, 0)
EMPTY = (0, 0, 0)
FOOD = (255, 0, 0)
CELL_GRID = (20, 20)
CELL_SIZE = (SCREEN_WIDTH / CELL_GRID[0], SCREEN_HEIGHT / CELL_GRID[1])


class BaseSnake:
    def __init__(self):
        self.initpygame()
        self.game_reset()

    def initpygame(self):
        pygame.init()
        pygame.display.set_caption("Snake AI")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    def game_reset(self):
        self.snake: deque[Vector] = deque()
        self.snake.append(Vector(CELL_GRID[0] // 2, CELL_GRID[1] // 2))
        self.points = 0
        self.rand_food()
        self.done = False
        self.direction = Vector(1, 0)

    def handle_keydown(self, key):
        if key == pygame.K_q:
            self.running = False

    def handle_action(self, action: Action):
        dx, dy = self.direction.x, self.direction.y
        if action == Action.LEFT:
            self.direction = Vector(-dy, dx)
        elif action == Action.RIGHT:
            self.direction = Vector(dy, -dx)
        elif action == Action.STRAIGHT:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def rand_food(self):
        while True:
            x = random.randrange(CELL_GRID[0])
            y = random.randrange(CELL_GRID[1])
            self.food = Vector(x, y)
            if not self.snake == self.food:
                break

    def get_distance(self) -> int:
        return abs(self.snake[0].x - self.food.x) + abs(self.snake[0].y - self.food.y)

    def step(self, action: Action) -> tuple[tuple, float, bool]:
        old_distance = self.get_distance()
        self.handle_events()
        self.handle_action(action)
        self.snake = self.snake + self.direction
        done = False

        if self.snake == self.food:
            self.points += 1
            self.rand_food()

            done = True
        self.draw()
        self.clock.tick(FPS)
        return (tuple(self.get_state()), reward, done)

    def get_state(self) -> tuple:
        return ()

    def get_reward(self, old_distance: int) -> float:
        return 0

    def reset(self):
        self.rand_food()
        self.snake = Vector(CELL_GRID[0] // 2, CELL_GRID[1] // 2)
        self.points = 0

    def draw(self):
        self.screen.fill(EMPTY)
        # Draw snake
        snake_rect = pygame.Rect(
            self.snake.x * CELL_SIZE[0],
            self.snake.y * CELL_SIZE[1],
            CELL_SIZE[0],
            CELL_SIZE[1],
        )
        pygame.draw.rect(self.screen, SNAKE, snake_rect)

        # Draw food
        food_rect = pygame.Rect(
            self.food.x * CELL_SIZE[0],
            self.food.y * CELL_SIZE[1],
            CELL_SIZE[0],
            CELL_SIZE[1],
        )
        pygame.draw.rect(self.screen, FOOD, food_rect)

        pygame.display.flip()
