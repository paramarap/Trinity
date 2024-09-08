import pygame
import math
import sys

pygame.init()

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
            display_text("Game Over - Press SPACE To Restart", (0, 0, 255), 30)
       
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