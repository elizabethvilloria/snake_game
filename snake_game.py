import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = [1, 0]  # Start moving right
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check for collisions with walls
        if (new_head[0] < 0 or new_head[0] >= GRID_COUNT or
            new_head[1] < 0 or new_head[1] >= GRID_COUNT):
            return False

        # Check for collisions with self
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] != -self.direction[0] or 
            new_direction[1] != -self.direction[1]):
            self.direction = new_direction

class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(0, GRID_COUNT - 1)
        y = random.randint(0, GRID_COUNT - 1)
        return (x, y)

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction([0, -1])
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction([0, 1])
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction([-1, 0])
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction([1, 0])
                elif event.key == pygame.K_SPACE:
                    # Reset game
                    snake.reset()
                    food.position = food.generate_position()
                    score = 0
                    game_over = False

        if not game_over:
            # Move snake
            if not snake.move():
                game_over = True

            # Check for food collision
            if snake.body[0] == food.position:
                snake.grow = True
                food.position = food.generate_position()
                score += 1

        # Draw everything
        screen.fill(BLACK)
        
        # Draw snake
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN,
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                            GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw food
        pygame.draw.rect(screen, RED,
                        (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE,
                         GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            screen.blit(game_over_text, (WINDOW_SIZE//2 - 200, WINDOW_SIZE//2))

        pygame.display.flip()
        clock.tick(10)  # Control game speed

if __name__ == "__main__":
    main() 