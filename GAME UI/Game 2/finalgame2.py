import pygame
import random

pygame.init()

SCREEN_WIDTH = 850
SCREEN_HEIGHT = 850
ASTEROID_SIZE = 50
STARTING_ASTEROIDS = 3
LIVES = 3
FPS = 60
SPEED_INCREMENT_INTERVAL = 6000

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")

font = pygame.font.SysFont("timesnewroman", 25)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface([ASTEROID_SIZE, ASTEROID_SIZE])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ASTEROID_SIZE)
        self.rect.y = -ASTEROID_SIZE
        self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            global lives
            lives -= 1
            if lives < 0:
                lives = 0

def spawn_asteroids(num_asteroids, speed):
    for _ in range(num_asteroids):
        asteroid = Asteroid(speed)
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

def reset_game():
    global score, lives, asteroid_speed, last_speed_increment_time
    score = 0
    lives = LIVES
    asteroid_speed = 2
    last_speed_increment_time = pygame.time.get_ticks()
    all_sprites.empty()
    asteroids.empty()
    spawn_asteroids(STARTING_ASTEROIDS, asteroid_speed)

def start_screen():
    screen.fill(BLACK)
    start_text = font.render("Press SPACE to Start", True, GREEN)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

score = 0
lives = LIVES
asteroid_speed = 2
last_speed_increment_time = pygame.time.get_ticks()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

start_screen()
reset_game()

running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                    game_over = False
                else:
                    # If not game over, you might want to handle game events differently
                    pass
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in asteroids if s.rect.collidepoint(pos)]
            if clicked_sprites:
                for sprite in clicked_sprites:
                    sprite.kill()
                    score += 1
                    asteroid = Asteroid(asteroid_speed)
                    all_sprites.add(asteroid)
                    asteroids.add(asteroid)

    if not game_over:
        all_sprites.update()

        if lives == 0:
            game_over = True

        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increment_time > SPEED_INCREMENT_INTERVAL:
            asteroid_speed += 1
            last_speed_increment_time = current_time

        screen.fill(BLACK)

        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, GREEN)
        lives_text = font.render(f"Lives: {lives}", True, GREEN)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

    if game_over:
        game_over_text = font.render("You Lost! Press SPACE to Restart", True, GREEN)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()