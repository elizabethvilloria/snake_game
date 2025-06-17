import pygame
import random
import sys
import json
import os

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

food_color = RED
snake_color = GREEN

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")

# Load sound (fix file name)
eat_sound = pygame.mixer.Sound('eat_sound.wav')

def load_high_score():
    try:
        with open('high_score.json', 'r') as f:
            return json.load(f)['high_score']
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_high_score(score):
    with open('high_score.json', 'w') as f:
        json.dump({'high_score': score}, f)

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

    def generate_position(self, snake_body=None):
        while True:
            x = random.randint(0, GRID_COUNT - 1)
            y = random.randint(0, GRID_COUNT - 1)
            position = (x, y)
            if snake_body is None or position not in snake_body:
                return position

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    high_score = load_high_score()
    game_over = False
    paused = False
    game_speed = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif not game_over and not paused:
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
                    food.position = food.generate_position(snake.body)
                    score = 0
                    game_over = False
                    paused = False
                    game_speed = 10

        if not game_over and not paused:
            # Move snake
            if not snake.move():
                game_over = True
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)

            # Check for food collision
            if snake.body[0] == food.position:
                snake.grow = True
                food.position = food.generate_position(snake.body)
                score += 1
                eat_sound.play()
                # Make food a random color, but mistakenly also change snake color
                food_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                snake_color = GREEN
                # Increase speed every 5 points
                if score % 5 == 0:
                    game_speed += 1

        # Draw everything
        screen.fill(BLACK)
        
        # Draw snake
        for i, segment in enumerate(snake.body):
            pygame.draw.rect(screen, snake_color,
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                            GRID_SIZE - 2, GRID_SIZE - 2))
            # Draw eyes (face) only on the head
            if i == 0:
                eye_radius = 3
                eye_offset_x = 5
                eye_offset_y = 5
                eye1_center = (segment[0] * GRID_SIZE + eye_offset_x, segment[1] * GRID_SIZE + eye_offset_y)
                eye2_center = (segment[0] * GRID_SIZE + GRID_SIZE - eye_offset_x, segment[1] * GRID_SIZE + eye_offset_y)
                pygame.draw.circle(screen, WHITE, eye1_center, eye_radius)
                pygame.draw.circle(screen, WHITE, eye2_center, eye_radius)

        # Draw food
        pygame.draw.rect(screen, food_color,
                        (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE,
                         GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw score and high score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        if game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            screen.blit(game_over_text, (WINDOW_SIZE//2 - 200, WINDOW_SIZE//2))

        if paused:
            pause_text = font.render('PAUSED - Press P to continue', True, WHITE)
            screen.blit(pause_text, (WINDOW_SIZE//2 - 150, WINDOW_SIZE//2 + 50))

        pygame.display.flip()
        clock.tick(game_speed)  # Control game speed

if __name__ == "__main__":
    main() 