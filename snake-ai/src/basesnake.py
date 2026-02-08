from collections import deque
import random
from model import Vector, Action
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
FPS = 6
SNAKE = (0, 255, 0)
EMPTY = (0, 0, 0)
FOOD = (255, 0, 0)
CELL_GRID = (20, 20)
CELL_SIZE = (SCREEN_WIDTH / CELL_GRID[0], SCREEN_HEIGHT / CELL_GRID[1])


class BaseSnake:
    """Base Snake game environment with Pygame rendering and game state management."""

    def __init__(self):
        """Initialize the game environment and reset game state."""
        self._init_pygame()
        self.reset()

    def _init_pygame(self):
        """Initialize Pygame display and clock."""
        pygame.init()
        pygame.display.set_caption("Snake AI")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    def reset(self):
        """Reset the game to initial state."""
        self.snake: deque[Vector] = deque()
        self.snake.append(Vector(CELL_GRID[0] // 2, CELL_GRID[1] // 2))
        self.points = 0
        self.direction = Vector(1, 0)
        self._spawn_food()

    def handle_action(self, action: Action) -> None:
        """Apply the given action to change snake direction.

        Args:
            action: LEFT, RIGHT, or STRAIGHT action to apply.
        """
        dx, dy = self.direction.x, self.direction.y
        if action == Action.LEFT:
            self.direction = Vector(-dy, dx)
        elif action == Action.RIGHT:
            self.direction = Vector(dy, -dx)

    def handle_events(self) -> None:
        """Handle pygame events like quit and keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _spawn_food(self) -> None:
        """Spawn food at a random location not occupied by the snake."""
        while True:
            self.food = Vector(
                random.randrange(CELL_GRID[0]), random.randrange(CELL_GRID[1])
            )
            if self.food not in self.snake:
                break

    def _get_distance_to_food(self) -> int:
        """Calculate Manhattan distance from snake head to food.

        Returns:
            Manhattan distance as integer.
        """
        head = self.snake[0]
        return abs(head.x - self.food.x) + abs(head.y - self.food.y)

    def _move_snake(self) -> None:
        """Move snake in the current direction, adding head and removing tail if no food eaten."""
        target = self.snake[0] + self.direction
        self.snake.appendleft(target)
        if target != self.food:
            self.snake.pop()

    def step(self, action: Action) -> tuple[tuple, float, bool]:
        """Execute one game step.

        Args:
            action: Action to take.

        Returns:
            Tuple of (state, reward, done).
        """
        old_distance = self._get_distance_to_food()
        self.handle_events()
        self.handle_action(action)
        self._move_snake()
        done = self._check_game_over()
        self._render()
        self.clock.tick(FPS)
        return (tuple(self.get_state()), self.get_reward(old_distance), done)

    def _check_game_over(self) -> bool:
        """Check if game is over due to collision or food consumption.

        Returns:
            True if game is over, False otherwise.
        """
        head = self.snake[0]

        # Check boundaries
        if not self._is_within_bounds(head):
            return True

        # Check self collision
        if self._check_self_collision(head):
            return True

        # Check food collision
        if head == self.food:
            self.points += 1
            self._spawn_food()

        return False

    def _is_within_bounds(self, position: Vector) -> bool:
        """Check if position is within game boundaries.

        Args:
            position: Vector position to check.

        Returns:
            True if within bounds, False otherwise.
        """
        return 0 <= position.x < CELL_GRID[0] and 0 <= position.y < CELL_GRID[1]

    def _check_self_collision(self, head: Vector) -> bool:
        """Check if head collides with snake body.

        Args:
            head: Snake head position.

        Returns:
            True if collision detected, False otherwise.
        """
        return len(self.snake) > 1 and head in list(self.snake)[1:]

    def get_state(self) -> tuple:
        """Get current game state representation.

        Returns:
            State tuple (to be implemented by subclasses).
        """
        return ()

    def get_reward(self, old_distance: int) -> float:
        """Calculate reward for current step.

        Args:
            old_distance: Previous distance to food.

        Returns:
            Reward value (to be implemented by subclasses).
        """
        return 0

    def _render(self) -> None:
        """Render the game state to screen."""
        self.screen.fill(EMPTY)
        self._draw_snake()
        self._draw_food()
        pygame.display.flip()

    def _draw_snake(self) -> None:
        """Draw snake segments on screen."""
        for cell in self.snake:
            rect = pygame.Rect(
                cell.x * CELL_SIZE[0],
                cell.y * CELL_SIZE[1],
                CELL_SIZE[0],
                CELL_SIZE[1],
            )
            pygame.draw.rect(self.screen, SNAKE, rect)

    def _draw_food(self) -> None:
        """Draw food on screen."""
        rect = pygame.Rect(
            self.food.x * CELL_SIZE[0],
            self.food.y * CELL_SIZE[1],
            CELL_SIZE[0],
            CELL_SIZE[1],
        )
        pygame.draw.rect(self.screen, FOOD, rect)


def get_direction_from_keyboard() -> Action:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return Action.LEFT
            elif event.key == pygame.K_RIGHT:
                return Action.RIGHT
    return Action.STRAIGHT
