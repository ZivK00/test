import random
import sys
from typing import List, Tuple

import pygame


CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
MOVE_TICK = 10  # Frames per second

BACKGROUND_COLOR = (30, 30, 30)
SNAKE_COLOR = (34, 139, 34)
FOOD_COLOR = (220, 20, 60)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (240, 240, 240)

Direction = Tuple[int, int]


class SnakeGame:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 18)
        self.reset()

    def reset(self) -> None:
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake: List[Tuple[int, int]] = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction: Direction = (1, 0)  # moving right
        self.pending_direction: Direction = self.direction
        self.food = self._spawn_food()
        self.score = 0
        self.game_over = False

    def _spawn_food(self) -> Tuple[int, int]:
        available = {
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        } - set(self.snake)
        return random.choice(list(available))

    def _handle_direction(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_UP:
            new_direction = (0, -1)
        elif event.key == pygame.K_DOWN:
            new_direction = (0, 1)
        elif event.key == pygame.K_LEFT:
            new_direction = (-1, 0)
        elif event.key == pygame.K_RIGHT:
            new_direction = (1, 0)
        else:
            return

        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.pending_direction = new_direction

    def _move_snake(self) -> None:
        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.game_over = True
            return

        will_eat = new_head == self.food
        body_to_check = self.snake if will_eat else self.snake[:-1]
        if new_head in body_to_check:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if will_eat:
            self.score += 1
            self.food = self._spawn_food()
        else:
            self.snake.pop()

    def _draw_grid(self) -> None:
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def _draw_snake(self) -> None:
        for segment in self.snake:
            x, y = segment
            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(self.screen, SNAKE_COLOR, rect)

    def _draw_food(self) -> None:
        x, y = self.food
        rect = pygame.Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(self.screen, FOOD_COLOR, rect)

    def _draw_text(self) -> None:
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            message = "Game over — press R to restart or Esc to quit"
            game_over_text = self.font.render(message, True, TEXT_COLOR)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

    def _handle_game_over(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_r:
            self.reset()
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        self._handle_game_over(event)
                    else:
                        self._handle_direction(event)

            if not self.game_over:
                self._move_snake()

            self.screen.fill(BACKGROUND_COLOR)
            self._draw_grid()
            self._draw_snake()
            self._draw_food()
            self._draw_text()

            pygame.display.flip()
            self.clock.tick(MOVE_TICK)


def main() -> None:
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
