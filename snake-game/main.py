import pygame
import random
import sys

# -----------------------------
# Constants
# -----------------------------
WIDTH, HEIGHT = 800, 600
SNAKE_SIZE = 20

BASE_SPEED = 12           # initial speed
SPEED_INCREMENT = 0.25    # speed added per food

# Colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
GOLD   = (255, 215, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font_big = pygame.font.Font(None, 72)
font = pygame.font.Font(None, 36)


# -----------------------------
# Helper Functions
# -----------------------------
def spawn_food():
    """Normal food."""
    x = random.randrange(0, WIDTH // SNAKE_SIZE) * SNAKE_SIZE
    y = random.randrange(0, HEIGHT // SNAKE_SIZE) * SNAKE_SIZE
    return x, y


def spawn_special_food():
    """Golden food with +3 score."""
    return spawn_food()


def draw_snake(body):
    """Draws a snake with color gradient."""
    for i, (x, y) in enumerate(body):
        intensity = 50 + i * 2
        color = (0, min(255, intensity), 0)
        pygame.draw.rect(screen, color, [x, y, SNAKE_SIZE, SNAKE_SIZE])


def text_center(text, size, y):
    surface = pygame.font.Font(None, size).render(text, True, WHITE)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)


def wait_for_space():
    """Pause screen until SPACE is pressed."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        pygame.display.update()


# -----------------------------
# Main Game Function
# -----------------------------
def game_loop():
    # Initial variables
    snake_x, snake_y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0

    snake_body = [(snake_x, snake_y)]
    snake_length = 1

    food_x, food_y = spawn_food()
    special_food = False
    special_timer = 0

    score = 0
    speed = BASE_SPEED

    running = True

    while running:
        # ---------------- Input ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -SNAKE_SIZE, 0
                if event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = SNAKE_SIZE, 0
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -SNAKE_SIZE
                if event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, SNAKE_SIZE

        # ---------------- Update Snake ----------------
        snake_x = (snake_x + dx) % WIDTH
        snake_y = (snake_y + dy) % HEIGHT

         # --------------- FIXED FOOD COLLISION LOGIC ----------------

        # SPECIAL FOOD collision FIRST
        if special_food and snake_x == food_x and snake_y == food_y:
            score += 3
            snake_length += 3
            special_food = False
            food_x, food_y = spawn_food()

        # NORMAL FOOD collision
        elif snake_x == food_x and snake_y == food_y:
            score += 1
            snake_length += 1
            speed = BASE_SPEED + score * SPEED_INCREMENT

            # Chance to spawn special food
            if random.random() < 0.1:
                special_food = True
                special_timer = 50
                food_x, food_y = spawn_special_food()
            else:
                food_x, food_y = spawn_food()

        # Special food timer countdown
        if special_food:
            special_timer -= 1
            if special_timer <= 0:
                special_food = False
                food_x, food_y = spawn_food()

        # -----------------------------------------------------------

        # Update body
        snake_body.append((snake_x, snake_y))
        if len(snake_body) > snake_length:
            snake_body.pop(0)

        # Self-collision
        if snake_body.count((snake_x, snake_y)) > 1:
            running = False

        # ---------------- Draw Everything ----------------
        screen.fill(BLACK)

        draw_snake(snake_body)

        if special_food:
            pygame.draw.rect(screen, GOLD, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])
        else:
            pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])

        # Score
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

        pygame.display.update()
        clock.tick(speed)

    # ---------------- Game Over ----------------
    screen.fill(BLACK)
    text_center("GAME OVER", 72, HEIGHT // 2 - 40)
    text_center(f"Score: {score}", 48, HEIGHT // 2 + 20)
    text_center("Press SPACE to play again", 36, HEIGHT // 2 + 70)
    pygame.display.update()

    wait_for_space()
    game_loop()  # restart


# -----------------------------
# Start Screen
# -----------------------------
screen.fill(BLACK)
text_center("SNAKE GAME", 72, HEIGHT // 2 - 40)
text_center("Press SPACE to Start", 48, HEIGHT // 2 + 20)
pygame.display.update()

wait_for_space()
game_loop()
