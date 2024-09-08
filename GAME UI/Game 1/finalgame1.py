import sys
import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 850, 850
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Untouchables")

red = (255, 0, 0)

def draw(player, elapsed_time, attempts, stars, lost_text=None, hide_text=False):
    WIN.fill("black")

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "red")
    WIN.blit(time_text, (8, 8))

    attempts_text = FONT.render(f"Attempts: {attempts}", 1, "red")
    WIN.blit(attempts_text, (8, 40))

    pygame.draw.rect(WIN, red, player)

    for star in stars:
        pygame.draw.rect(WIN, "red", star)

    if lost_text:
        WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))

    pygame.display.update()

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60
PLAYER_VEL = 7

STAR_WIDTH = 12
STAR_HEIGHT = 12
STAR_VEL = 12

FONT = pygame.font.SysFont("timesnewroman", 25)

pygame.display.update()

def start_screen():
    start_text = FONT.render("Press SPACE to Start", 1, "red")
    WIN.blit(start_text, (WIDTH/2 - start_text.get_width()/2, HEIGHT/2 - start_text.get_height()/2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def game_over_screen(attempts):
    game_over_text = FONT.render("Game Over - Press SPACE to Restart", 1, "red")
    WIN.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))

    attempts_text = FONT.render(f"Attempts: {attempts}", 1, "red")
    WIN.blit(attempts_text, (WIDTH/2 - attempts_text.get_width()/2, HEIGHT/2 + game_over_text.get_height()/2 + 10))

    pygame.display.update()

    space_pressed = False

    while not space_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                space_pressed = True

def main():
    run = True
    attempts = 0
    player = pygame.Rect(225, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    star_add_increment = 2500
    star_count = 0
    stars = []
    hit = False
    start_time = None
    lost_text = None
    hide_text = False

    start_screen()

    while run:
        star_count += clock.tick(60)

        if start_time is None or hit:
            start_time = time.time()
            hit = False
            attempts += 1

            star_add_increment = 2500
            star_count = 0
            stars = []
            hide_text = False

        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(5):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(300, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = time.time()
                stars = []
                lost_text = None
                hide_text = True

            if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                    hide_text = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True

        if hit:
            game_over_screen(attempts)

        draw(player, elapsed_time, attempts, stars, lost_text, hide_text)
       
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    main()