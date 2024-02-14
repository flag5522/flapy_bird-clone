import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer for Sound
pygame.mixer.init()

# Game Window
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
SKY_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 128, 0)  # Color for the mountains
ORANGE = (255, 140, 0)  # Color for the bird

# Cloud Class for Background
class Cloud:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.size = random.randint(50, 100)

    def update(self):
        self.x -= 2  # Slower than mountains
        if self.x < -self.size:
            self.x = SCREEN_WIDTH + self.size
            self.y = random.randint(0, SCREEN_HEIGHT // 2)

    def draw(self):
        pygame.draw.circle(screen, GREY, (self.x, self.y), self.size)

# Bird Class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.radius = 15
        self.jumpSpeed = 10
        self.gravity = 2
        self.isJumping = False

    def jump(self):
        self.isJumping = True
        self.jumpSpeed = 10

    def update(self):
        if self.isJumping:
            self.jumpSpeed -= 1
            self.y -= self.jumpSpeed
            if self.jumpSpeed < -10:
                self.isJumping = False
        else:
            self.y += self.gravity

    def draw(self):
        pygame.draw.circle(screen, ORANGE, (self.x, self.y), self.radius)
        # Small eye
        pygame.draw.circle(screen, BLACK, (self.x + 5, self.y - 5), 2)

# Pylon Class
class Pylon:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(-150, 150)
        self.width = 30
        self.height = 300
        self.gap = 200

    def update(self):
        self.x -= 2
        if self.x < -self.width:
            self.x = SCREEN_WIDTH
            self.y = random.randint(-150, 150)

    def collide(self, bird):
        if bird.y - bird.radius < self.y + self.height or bird.y + bird.radius > self.y + self.height + self.gap:
            if bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width:
                return True
        return False

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, 0, self.width, self.height + self.y))
        pygame.draw.rect(screen, BLACK, (self.x, self.height + self.gap + self.y, self.width, SCREEN_HEIGHT - (self.height + self.gap + self.y)))

# Function to Draw Mountains (less steep and more gradual)
def draw_mountains():
    mountain_points = [
        (0, SCREEN_HEIGHT),
        (100, 400),
        (200, SCREEN_HEIGHT),
        (300, 450),
        (400, SCREEN_HEIGHT),
        (500, 400),
        (600, SCREEN_HEIGHT)
    ]
    pygame.draw.polygon(screen, GREEN, mountain_points)

# Load the Game Over Sound
game_over_sound = pygame.mixer.Sound("GO.wav")

# Load the New High Score Sound
new_high_score_sound = pygame.mixer.Sound("nhs.wav")

# Initialize Bird and Pylons
bird = Bird()
pylons = [Pylon(300), Pylon(600), Pylon(900)]

# Initialize Clouds
clouds = [Cloud() for _ in range(5)]

# Scoring
score = 0
high_score = 0
score_card = pygame.Surface((200, 100))
score_card.fill(WHITE)

# High Score File
high_score_file = "high_score.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        high_score = int(file.read())

# Game Over Card
game_over_card = pygame.Surface((200, 100))
game_over_card.fill(WHITE)
font = pygame.font.SysFont(None, 24)
game_over_text = font.render("Game Over", True, BLACK)
score_text = font.render(f"Score: {score}", True, BLACK)
high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
restart_text = font.render("Press 'R' to Restart", True, BLACK)
game_over_card.blit(game_over_text, (80, 10))
game_over_card.blit(score_text, (80, 30))
game_over_card.blit(high_score_text, (80, 50))
game_over_card.blit(restart_text, (80, 70))

# Game State
game_over = False
new_high_score = False

# Main Game Loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    screen.fill(SKY_BLUE)

    # Draw Mountains
    draw_mountains()

    # Draw Clouds
    for cloud in clouds:
        cloud.update()
        cloud.draw()

    if not game_over:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update Bird and Pylons
        bird.update()
        for pylon in pylons:
            pylon.update()
            if pylon.collide(bird):
                # Play Game Over Sound
                game_over_sound.play()

                # Game Over State
                game_over = True

                # Check for New High Score
                if score > high_score:
                    high_score = score
                    new_high_score = True

                # Reset Game
                bird = Bird()
                pylons = [Pylon(300), Pylon(600), Pylon(900)]

            if pylon.x == bird.x:
                score += 1

    if game_over:
        # Display Game Over Card
        screen.blit(game_over_card, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        # Event Handling for Restart
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    score = 0
                    bird = Bird()
                    pylons = [Pylon(300), Pylon(600), Pylon(900)]

                    if new_high_score:
                        # Play New High Score Sound
                        new_high_score_sound.play()
                        new_high_score = False

    # Draw Bird and Pylons
    bird.draw()
    for pylon in pylons:
        pylon.draw()

    # Draw Score Card
    screen.blit(score_card, (10, 10))
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(high_score_text, (20, 50))

    pygame.display.update()

# Save High Score
with open(high_score_file, "w") as file:
    file.write(str(high_score))

pygame.quit()
