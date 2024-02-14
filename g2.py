import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Game Window
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Drone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Cloud Class for Background
class Cloud:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.size = random.randint(50, 100)

    def update(self):
        self.x -= 1
        if self.x < -self.size:
            self.x = SCREEN_WIDTH + self.size
            self.y = random.randint(0, SCREEN_HEIGHT // 2)

    def draw(self):
        pygame.draw.circle(screen, GREY, (self.x, self.y), self.size)

# Drone Class
class Drone:
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

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 30, 30))  # Simple drone representation

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

    def collide(self, drone):
        if drone.y < self.y + self.height or drone.y + 30 > self.y + self.height + self.gap:
            if drone.x > self.x and drone.x < self.x + self.width:
                return True
        return False

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, 0, self.width, self.height + self.y))
        pygame.draw.rect(screen, BLACK, (self.x, self.height + self.gap + self.y, self.width, SCREEN_HEIGHT - (self.height + self.gap + self.y)))

# Initialize Drone and Pylons
drone = Drone()
pylons = [Pylon(300), Pylon(600), Pylon(900)]

# Initialize Clouds
clouds = [Cloud() for _ in range(5)]

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
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                drone.jump()

    # Update Drone and Pylons
    drone.update()
    for pylon in pylons:
        pylon.update()
        if pylon.collide(drone):
            # Reset Game
            score = 0
            drone = Drone()
            pylons = [Pylon(300), Pylon(600), Pylon(900)]
        if pylon.x == drone.x:
            score += 1
            if score > high_score:
                high_score = score

    # Draw Clouds
    for cloud in clouds:
        cloud.update()
        cloud.draw()

    # Draw Drone and Pylons
    drone.draw()
    for pylon in pylons:
        pylon.draw()

    # Display Score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    pygame.display.update()

# Save High Score
with open(high_score_file, "w") as file:
    file.write(str(high_score))

pygame.quit()
