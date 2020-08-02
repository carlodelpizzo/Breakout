import pygame
import random
import math
from pygame.locals import *

pygame.init()

# Initialize Screen
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# Title
pygame.display.set_caption("Shitty Breakout")
# Screen Colors
bgColor = [0, 0, 0]
fgColor = [50, 100, 200]
# Font
font_size = 25
font = pygame.font.SysFont("", font_size)


class MultiBall:

    def __init__(self, direction):
        self.radius = 15
        self.x = screen_width / 2
        self.y = bricks[len(bricks) - 1].y + bricks[len(bricks) - 1].height + self.radius
        self.direction = direction
        self.g = 0

    def move(self):
        self.gravity()
        self.bounce_wall()
        self.bounce_paddle()
        self.update_pos(self.x + self.speed_limit_x(self.direction[0]), self.y + self.speed_limit_y(self.direction[1]))

    def clear(self):
        if self.collide_paddle(player.x, player.y, player.width):
            pygame.draw.circle(screen, bgColor, (int(self.x), int(self.y)), self.radius)
            player.draw()
        else:
            pygame.draw.circle(screen, bgColor, (int(self.x), int(self.y)), self.radius)

    def draw(self):
        pygame.draw.circle(screen, fgColor, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        # self.__init__((random.randint(-3, 3), random.randint(1, 2)))
        self.__init__((0, 1))

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def speed_limit_x(self, x_dir):
        max_x_speed = 4
        if self.direction[0] > max_x_speed:
            limited_x = max_x_speed
        elif self.direction[0] < -max_x_speed:
            limited_x = -max_x_speed
        else:
            limited_x = x_dir
        return limited_x

    def speed_limit_y(self, y_dir):
        max_y_speed = 5
        if self.direction[1] > max_y_speed:
            limited_y = max_y_speed
        elif self.direction[1] < -max_y_speed:
            limited_y = -max_y_speed
        else:
            limited_y = y_dir
        return limited_y

    def bounce_wall(self):
        # if left of screen
        if self.x <= self.radius:
            self.direction = (-self.direction[0], self.direction[1])
            self.update_pos(self.radius, self.y)
        # if right of screen
        elif self.x >= screen_width - self.radius:
            self.direction = (-self.direction[0], self.direction[1])
            self.update_pos((screen_width - self.radius), self.y)
        # if above screen
        if self.y <= self.radius:
            self.direction = (self.direction[0], -self.direction[1])
            self.update_pos(self.x, self.radius)
        # if below screen
        if self.y >= screen_height - self.radius:
            self.reset()

    def bounce_paddle(self):
        boost_x = (player.speed / 2.5)
        boost_y = (player.speed / 6)
        if self.collide_paddle(player.x, player.y, player.width):
            self.update_pos(self.x, player.y - self.radius)
            if player.direction != "":
                # if ball direction == right
                if self.direction[0] >= 0 and player.direction == "right":
                    self.direction = (self.direction[0] + boost_x, self.direction[1])
                    self.direction = (self.direction[0], -(self.direction[1] + boost_y))
                elif self.direction[0] >= 0 and player.direction == "left":
                    self.direction = (self.direction[0] - boost_x, self.direction[1])
                    self.direction = (self.direction[0], -(self.direction[1] - boost_y))
                # if ball direction == left
                elif self.direction[0] < 0 and player.direction == "right":
                    self.direction = (self.direction[0] + boost_x, self.direction[1])
                    self.direction = (self.direction[0], -(self.direction[1] - boost_y))
                elif self.direction[0] < 0 and player.direction == "left":
                    self.direction = (self.direction[0] - boost_x, self.direction[1])
                    self.direction = (self.direction[0], -(self.direction[1] + boost_y))
            else:
                self.direction = (self.direction[0], -self.direction[1])

    def collide_paddle(self, paddle_x, paddle_y, paddle_w):
        if paddle_x + paddle_w + self.radius >= self.x >= paddle_x - self.radius and self.y >= paddle_y - self.radius:
            self.direction = (self.speed_limit_x(self.direction[0]), self.speed_limit_y(self.direction[1]))
            return True
        else:
            return False

    def collide_ball(self):
        for i in range(len(multi_ball)):
            if self.x != multi_ball[i].x and self.y != multi_ball[i].y:
                if multi_ball[i].x + multi_ball[i].radius + self.radius >= self.x:
                    if self.x >= multi_ball[i].x - multi_ball[i].radius - self.radius:
                        if multi_ball[i].y + multi_ball[i].radius + self.radius >= self.y:
                            if self.y >= multi_ball[i].y - multi_ball[i].radius - self.radius:
                                multi_ball[i].draw()
                                return True
            else:
                return False

    def gravity(self):
        gravity = (0.12 / frame_rate)
        if self.collide_paddle(player.x, player.y, player.width):
            self.direction = (self.direction[0], self.direction[1] + self.g)
            self.g = 0
        elif -0.01 <= self.direction[1] <= 0.01:
            self.direction = (self.direction[0], self.direction[1] + self.g)
            self.g -= self.g / 3
        else:
            self.g += gravity
            self.direction = (self.direction[0], self.direction[1] + self.g)


class Player:

    def __init__(self, x, y, width, height, direction, speed):
        self.x = x - width / 2
        self.y = y - height / 2
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed
        self.boost = False
        self.color = fgColor

    def move(self):
        if self.direction == "left" and self.x >= 0:
            self.x -= self.speed
        elif self.direction == "right" and self.x <= screen_width - self.width:
            self.x += self.speed

    def clear(self):
        pygame.draw.rect(screen, bgColor, (int(self.x), int(self.y), self.width, self.height))

    def draw(self):
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.width, self.height))


class Brick:
    def __init__(self, x, y, width, height, level):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = fgColor
        self.level = level

    def draw(self):
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), int(self.width), int(self.height)))

    def clear(self):
        pygame.draw.rect(screen, bgColor, (int(self.x), int(self.y), self.width, self.height))


# Initialize Bricks (x, y, width, height, level)
bricks = []
brick_col = 10
brick_row = 3
brick_lvl = 2
segment = screen_width / brick_col
brick_w = segment * 0.70
brick_h = 20
brick_count = 0

for row in range(brick_row):
    for col in range(brick_col):
        bricks.append(brick_count)
        x_offset = (segment / 2) - (brick_w / 2) + (segment * col)
        y_offset = (segment - brick_w) + ((brick_h + segment - brick_w) * row)
        bricks[brick_count] = Brick(x_offset, y_offset, brick_w, brick_h, brick_lvl)
        brick_count += 1

# Initialize Ball (direction)
multi_ball = [0]
ball_count = 1
multi_ball[0] = MultiBall((0, 1))

# Initialize Paddle (x, y, width, height, direction, speed)
player = Player(screen_width / 2, screen_height - (screen_height / 30), 200, 20, "", 3)
player.draw()

# Game Loop
clock = pygame.time.Clock()
running = True
cheater = False
pause = False
shift_boost = 3
frame_rate = 240


def display_ball_stats():
    g_text = str(multi_ball[0].g)
    dx_text = str(multi_ball[0].direction[0])
    dy_text = str(multi_ball[0].direction[1])
    display_g = font.render("g: " + g_text[0:5], True, fgColor)
    if multi_ball[0].direction[0] >= 0:
        display_dx = font.render("x:  " + dx_text[0:5], True, fgColor)
    else:
        display_dx = font.render("x: " + dx_text[0:6], True, fgColor)
    if multi_ball[0].direction[1] >= 0:
        display_dy = font.render("y: " + dy_text[0:5], True, fgColor)
    else:
        display_dy = font.render("y: " + dy_text[0:6], True, fgColor)
    screen.blit(display_g, (0, 0))
    screen.blit(display_dx, (0, font_size))
    screen.blit(display_dy, (0, font_size * 2))


def cheater_mode():
    # Follow Ball
    if multi_ball[0].x < (player.x + player.width / 2) + 1:
        player.direction = "left"
    elif multi_ball[0].x > (player.x + player.width / 2) - 1:
        player.direction = "right"
    if (player.x + player.width / 2) - 1 <= multi_ball[0].x <= (player.x + player.width / 2) + 1:
        player.direction = ""
    # Give Ball x Momentum
    if player.direction == "":
        if multi_ball[0].collide_paddle(player.x, player.y, player.width):
            if multi_ball[0].direction[0] == 0:
                ran = random.randint(0, 10)
                if ran % 2 == 0:
                    player.direction = "left"
                else:
                    player.direction = "right"
    # Teleport to Ball
    if multi_ball[0].x > player.x + player.width + multi_ball[0].radius:
        player.clear()
        player.x = multi_ball[0].x - multi_ball[0].radius - player.width
        player.draw()
    if multi_ball[0].x < player.x:
        player.clear()
        player.x = multi_ball[0].x
        player.draw()
    # Emergency Teleport
    if multi_ball[0].y + multi_ball[0].radius >= screen_height - 1:
        if multi_ball[0].direction[0] >= 0:
            player.x = multi_ball[0].x - player.width / 2
            player.direction = "right"
        else:
            player.x = multi_ball[0].x - player.width / 2
            player.direction = "left"
    # Bound Player
    if player.x < 0:
        player.x = 0
    elif player.x > screen_width - player.width:
        player.x = screen_width - player.width


def cheater_mode_multi():
    for ball in range(len(multi_ball)):
        if multi_ball[ball].y + multi_ball[ball].radius >= player.y:
            if multi_ball[ball].direction[0] > 0:
                player.x = multi_ball[ball].x - player.width / 2
                player.direction = "right"
            elif multi_ball[ball].direction[0] < 0:
                player.x = multi_ball[ball].x - player.width / 2
                player.direction = "left"
            else:
                ran = random.randint(0, 2)
                player.x = multi_ball[ball].x - player.width / 2
                if ran % 2 == 0:
                    player.direction = "left"
                else:
                    player.direction = "right"
        if player.x < 0:
            player.x = 0
        elif player.x > screen_width - player.width:
            player.x = screen_width - player.width


def game_loop():
    screen.fill(bgColor)

    # Cheater Mode Act
    if cheater:
        # cheater_mode()
        cheater_mode_multi()

    # Player
    player.move()
    player.draw()

    # Brick
    for brick in range(brick_count):
        bricks[brick].draw()

    # Ball
    for i in range(ball_count):
        multi_ball[i].move()
    for i in range(ball_count):
        multi_ball[i].draw()

    # Cheater Mode Stop
    if cheater:
        player.direction = ""

    # display_ball_stats()
    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        # On Key Down
        if event.type == pygame.KEYDOWN:
            # Left/Right Movement
            if keys[K_LEFT] or keys[K_a]:
                if keys[K_RIGHT] or keys[K_d]:
                    player.direction = ""
                else:
                    player.direction = "left"
            elif keys[K_RIGHT] or keys[K_d]:
                if keys[K_LEFT] or keys[K_a]:
                    player.direction = ""
                else:
                    player.direction = "right"

            # Shift Boost
            if (keys[K_LSHIFT] or keys[K_RSHIFT]) and player.boost is False:
                player.speed += shift_boost
                player.boost = True

            # Cheater Mode
            if keys[K_c] and cheater is False:
                cheater = True
                player.clear()
                player.color = (255, 0, 0)
                player.draw()
            elif keys[K_c] and cheater is True:
                cheater = False
                player.clear()
                player.color = fgColor
                player.draw()

            # Add Ball
            if keys[K_b]:
                multi_ball.append(ball_count)
                # multi_ball[len(multi_ball) - 1] = Ball((random.randint(-3, 3), random.randint(1, 2)))
                multi_ball[len(multi_ball) - 1] = MultiBall((0, 1))
                ball_count += 1

            # Kill Ball
            if keys[K_k]:
                if len(multi_ball) > 1:
                    multi_ball.pop(len(multi_ball) - 1)
                    # multi_ball[len(multi_ball) - 1] = Ball((random.randint(-3, 3), random.randint(1, 2)))
                    ball_count -= 1

            # Pause
            if keys[K_SPACE] and pause is False:
                pause = True
            elif keys[K_SPACE] and pause is True:
                pause = False

            # Frame Advance
            if pause is True:
                if keys[K_n]:
                    game_loop()

        # On Key Up
        if event.type == pygame.KEYUP:
            # Left/Right Movement
            if player.direction == "left" and keys[K_LEFT] == 0 and keys[K_a] == 0:
                player.direction = ""
            elif player.direction == "right" and keys[K_RIGHT] == 0 and keys[K_d] == 0:
                player.direction = ""
            elif (keys[K_LEFT] or keys[K_a]) and (keys[K_RIGHT] == 0 or keys[K_d] == 0):
                player.direction = "left"
            elif (keys[K_RIGHT] or keys[K_d]) and (keys[K_LEFT] == 0 or keys[K_a] == 0):
                player.direction = "right"

            # Shift Boost
            if keys[K_LSHIFT] == 0 and keys[K_RSHIFT] == 0 and player.boost is True:
                player.speed -= shift_boost
                player.boost = False

    if pause is False:
        game_loop()
    clock.tick(frame_rate)
