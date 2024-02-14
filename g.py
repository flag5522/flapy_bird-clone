import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Game Window
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
BLUE = (135, 206, 235)
GREEN = (0, 255, 0)

# Bird Class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = 150
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

# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(-150, 150)
        self.width = 50
        self.height = 300
        self.gap = 200

    def update(self):
        self.x -= 2
        if self.x < -self.width:
            self.x = SCREEN_WIDTH
            self.y = random.randint(-150, 150)

    def collide(self, bird):
        if bird.y < self.y + self.height or bird.y + 30 > self.y + self.height + self.gap:
            if bird.x > self.x and bird.x < self.x + self.width:
                return True
        return False

# Initialize Bird and Pipes
bird = Bird()
pipes = [Pipe(300), Pipe(600), Pipe(900)]

# Scoring
score = 0
high_score = 0

# High Score File
high_score_file = "high_score.txt"

# Check if high score file exists
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        high_score = int(file.read())

# Main Game Loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    screen.fill(BLUE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # Update Bird and Pipes
    bird.update()
    for pipe in pipes:
        pipe.update()
        if pipe.collide(bird):
            # Reset Game
            score = 0
            bird = Bird()
            pipes = [Pipe(300), Pipe(600), Pipe(900)]
        if pipe.x == bird.x:
            score += 1
            if score > high_score:
                high_score = score

    # Draw Bird and Pipes
    pygame.draw.rect(screen, GREEN, (bird.x, bird.y, 30, 30))
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe.x, 0, pipe.width, pipe.height + pipe.y))
        pygame.draw.rect(screen, GREEN, (pipe.x, pipe.height + pipe.gap + pipe.y, pipe.width, SCREEN_HEIGHT))

    # Display Score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    pygame.display.update()

# Save High Score
with open(high_score_file, "w") as file:
    file.write(str(high_score))

pygame.quit()
