import sys
import pygame
import random
import time
import math

pygame.init()

SCREEN_WIDTH = 850
SCREEN_HEIGHT = 850
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Selector")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("timesnewroman", 25)

def draw_game_selection():
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, (80, 325, 200, 200))
    pygame.draw.rect(screen, GREEN, (325, 325, 200, 200))
    pygame.draw.rect(screen, BLUE, (570, 325, 200, 200))

    pygame.display.flip()

def game_one():
    WIDTH, HEIGHT = 850, 850
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Untouchables")

    PLAYER_WIDTH = 60
    PLAYER_HEIGHT = 60
    PLAYER_VEL = 7

    STAR_WIDTH = 12
    STAR_HEIGHT = 12
    STAR_VEL = 12

    FONT = pygame.font.SysFont("timesnewroman", 25)

    def draw(player, elapsed_time, attempts, stars, lost_text=None, hide_text=False):
        WIN.fill(BLACK)
        time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "red")
        WIN.blit(time_text, (8, 8))
        attempts_text = FONT.render(f"Attempts: {attempts}", 1, "red")
        WIN.blit(attempts_text, (8, 40))
        pygame.draw.rect(WIN, RED, player)
        for star in stars:
            pygame.draw.rect(WIN, "red", star)
        if lost_text:
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
        pygame.display.update()

    def start_screen():
        start_text = FONT.render("Press SPACE to Start", 1, "red")
        WIN.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2 - start_text.get_height() / 2))
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or pygame.K_ESCAPE:
                    waiting = False
            
    def game_over_screen(attempts):
        game_over_text = FONT.render("You Lost! Press SPACE to Restart", 1, "red")
        WIN.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - game_over_text.get_height() / 2))
        attempts_text = FONT.render(f"Attempts: {attempts}", 1, "red")
        WIN.blit(attempts_text, (WIDTH / 2 - attempts_text.get_width() / 2, HEIGHT / 2 + game_over_text.get_height() / 2 + 10))
        pygame.display.update()
        space_pressed = False
        while not space_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or pygame.K_ESCAPE:
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_time = time.time()
                        stars = []
                        lost_text = None
                        hide_text = True
                    if event.key == pygame.K_ESCAPE:
                        return
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

def game_two():
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

    global score, lives, asteroid_speed, last_speed_increment_time
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
                        pass
                elif event.key == pygame.K_ESCAPE:
                    return

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

def game_three():
    WIDTH, HEIGHT = 850, 850
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Brick Breaker")

    FPS = 60
    PADDLE_WIDTH = 80
    PADDLE_HEIGHT = 13
    BALL_RADIUS = 8

    LIVES_FONT = pygame.font.SysFont("timesnewroman", 25)
    FONT = pygame.font.SysFont("timesnewroman", 25)

    class Paddle:
        initial_VEL = 6
        VEL_increment_interval = 10000

        def __init__(self, x, y, width, height, color):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.VEL = self.initial_VEL
            self.last_VEL_increment_time = pygame.time.get_ticks()

        def draw(self, win):
            pygame.draw.rect(
                win, self.color, (self.x, self.y, self.width, self.height))

        def move(self, direction=1):
            self.x = self.x + self.VEL * direction

    class Ball:
        initial_VEL = 5.5
        VEL_increment_interval = 10000

        def __init__(self, x, y, radius, color):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            self.x_vel = 0
            self.y_vel = -self.initial_VEL
            self.speed_increment_interval = self.VEL_increment_interval
            self.last_speed_increment_time = pygame.time.get_ticks()

        def move(self):
            self.x += self.x_vel
            self.y += self.y_vel
            current_time = pygame.time.get_ticks()
            if current_time - self.last_speed_increment_time >= self.speed_increment_interval:
                self.initial_VEL += 1
                self.x_vel = 0
                self.y_vel = -self.initial_VEL
                self.speed_increment_interval += self.VEL_increment_interval
                self.last_speed_increment_time = current_time

        def set_vel(self, x_vel, y_vel):
            self.x_vel = x_vel
            self.y_vel = y_vel

        def draw(self, win):
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    class Brick:
        def __init__(self, x, y, width, height, health, colors):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.health = health
            self.max_health = health
            self.colors = colors
            self.color_index = 0

        def draw(self, win):
            pygame.draw.rect(
                win, self.colors[self.color_index], (self.x, self.y, self.width, self.height))

        def collide(self, ball):
            if not (ball.x <= self.x + self.width and ball.x >= self.x):
                return False
            if not (ball.y - ball.radius <= self.y + self.height):
                return False
            self.hit()
            ball.set_vel(ball.x_vel, ball.y_vel * -1)
            return True

        def hit(self):
            self.health -= 1
            self.color_index = min(
                self.health, len(self.colors) - 1)

    def draw(win, paddle, ball, bricks, lives):
        win.fill("black")
        paddle.draw(win)
        ball.draw(win)
        for brick in bricks:
            brick.draw(win)
        lives_text = LIVES_FONT.render(f"Lives: {lives}", 1, (0, 0, 255))
        win.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))
        pygame.display.update()

    def ball_collision(ball):
        if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH:
            ball.set_vel(ball.x_vel * -1, ball.y_vel)
        if ball.y - BALL_RADIUS <= 0:
            ball.set_vel(ball.x_vel, abs(ball.y_vel))

    def ball_paddle_collision(ball, paddle):
        if not (ball.x <= paddle.x + paddle.width and ball.x >= paddle.x):
            return
        if not (ball.y + ball.radius >= paddle.y):
            return
        paddle_center = paddle.x + paddle.width/2
        distance_to_center = ball.x - paddle_center
        percent_width = distance_to_center / paddle.width
        angle = percent_width * 90
        angle_radians = math.radians(angle)
        x_vel = math.sin(angle_radians) * ball.initial_VEL
        y_vel = math.cos(angle_radians) * ball.initial_VEL * -1
        ball.set_vel(x_vel, y_vel)

    def generate_bricks(rows, cols):
        gap = 2
        brick_width = WIDTH // cols - gap
        brick_height = 20
        bricks = []
        for row in range(rows):
            if row == 0:
                brick_health = 2
                brick_colors = [(0, 0, 255), (0, 0, 155)]
            else:
                brick_health = 2
                brick_colors = [(0, 0, 255), (0, 0, 155)]
            for col in range(cols):
                brick = Brick(col * brick_width + gap * col, row * brick_height +
                              gap * row, brick_width, brick_height, brick_health, brick_colors)
                bricks.append(brick)
        return bricks

    def display_text(text, color, font_size, y_offset=0):
        font = pygame.font.SysFont("timesnewroman", font_size)
        text_render = font.render(text, 1, color)
        WIN.blit(text_render, (WIDTH/2 - text_render.get_width()/2, HEIGHT/2 - text_render.get_height()/2 + y_offset))
        pygame.display.update()

    def start_screen():
        display_text("Press SPACE to Start", (0, 0, 255), 25)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or pygame.K_ESCAPE:
                    waiting = False

    def reset(paddle, ball):
        paddle.x = WIDTH/2 - PADDLE_WIDTH/2
        paddle.y = HEIGHT - PADDLE_HEIGHT - 5
        ball.x = WIDTH/2
        ball.y = paddle.y - BALL_RADIUS
        ball.initial_VEL = Ball.initial_VEL

    def main():
        clock = pygame.time.Clock()

        paddle_x = WIDTH/2 - PADDLE_WIDTH/2
        paddle_y = HEIGHT - PADDLE_HEIGHT - 5
        paddle = Paddle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, (0, 0, 255))
        ball = Ball(WIDTH/2, paddle_y - BALL_RADIUS, BALL_RADIUS, (0, 0, 255))
        bricks = generate_bricks(3, 10)

        lives = 3
        paused = False
        restart_text = False

        start_screen()

        while True:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if restart_text:
                            bricks = generate_bricks(3, 10)
                            lives = 3
                            reset(paddle, ball)
                            restart_text = False 
                        else:
                            paused = False
            if paused:
                screen.fill(BLACK)
                display_text("You Lost! Press SPACE to Restart", (0, 0, 255), 25)

            else:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT] and paddle.x - paddle.VEL >= 0:
                    paddle.move(-1)
                if keys[pygame.K_RIGHT] and paddle.x + paddle.width + paddle.VEL <= WIDTH:
                    paddle.move(1)

                ball.move()
                ball_collision(ball)
                ball_paddle_collision(ball, paddle)

                for brick in bricks[:]:
                    brick.collide(ball)

                    if brick.health <= 0:
                        bricks.remove(brick)

                if ball.y + ball.radius >= HEIGHT:
                    lives -= 1
                if lives <= 0:
                    restart_text = True
                    paused = True
                    if restart_text:
                        bricks = generate_bricks(3, 10)
                        lives = 3
                        reset(paddle, ball)
                        restart_text = False

                if len(bricks) == 0:
                    bricks = generate_bricks(3, 10)
                    lives = 3
                    reset(paddle, ball)
                    restart_text = True
                draw(WIN, paddle, ball, bricks, lives)

    if __name__ == "__main__":
        main()

def main():
    running = True
    while running:
        draw_game_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 80 <= x <= 280 and 325 <= y <= 525:
                    game_one()
                elif 325 <= x <= 525 and 325 <= y <= 525:
                    game_two()
                elif 570 <= x <= 770 and 325 <= y <= 525:
                    game_three()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()