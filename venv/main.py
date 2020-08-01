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
pygame.display.set_caption("Title")
# Screen Colors
bgColor = [0, 0, 0]
fgColor = [50, 100, 200]


class Ball:

    def __init__(self, direction):
        self.x = int(screen_width / 2)
        self.y = int(screen_height / 5)
        self.radius = 15
        self.direction = direction
        self.g = 0

    def move(self):
        self.clear()
        self.bounce_wall()
        self.bounce_paddle()
        self.gravity()
        self.speed_limit()
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.draw()

    def clear(self):
        if collide(self.x, self.y, self.radius, player.x, player.y, player.width):
            pygame.draw.circle(screen, bgColor, (self.x, self.y), self.radius)
            player.draw()
        else:
            pygame.draw.circle(screen, bgColor, (self.x, self.y), self.radius)

    def draw(self):
        pygame.draw.circle(screen, fgColor, (self.x, self.y), self.radius)

    def reset(self):
        self.__init__((random.randint(-3, 3), random.randint(1, 2)))

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def speed_limit(self):
        max_y_speed = 7
        max_x_speed = 5
        if self.direction[0] > max_x_speed:
            self.direction = (max_x_speed, self.direction[1])
        if self.direction[1] > max_y_speed:
            self.direction = (self.direction[0], max_y_speed)

    def bounce_wall(self):
        if self.x <= self.radius:
            self.direction = (-self.direction[0], self.direction[1])
            self.update_pos(self.radius, self.y)
        elif self.x >= screen_width - self.radius:
            self.direction = (-self.direction[0], self.direction[1])
            self.update_pos((screen_width - self.radius), self.y)
        if self.y <= self.radius:
            self.direction = (self.direction[0], -self.direction[1])
            self.update_pos(self.x, self.radius)
        if self.y >= screen_height - self.radius:
            self.reset()

    def bounce_paddle(self):
        # higher number = less boost
        boost_x = 300
        boost_y = 400
        if collide(self.x, self.y, self.radius, player.x, player.y, player.width):
            self.update_pos(self.x, player.y - self.radius)
            self.direction = (self.direction[0], -int(self.direction[1] + player.speed / boost_y))
            if player.direction != "":
                if self.direction[0] >= 0 and player.direction == "right":
                    self.direction = (self.direction[0] + int(player.speed / boost_x), self.direction[1])
                elif self.direction[0] >= 0 and player.direction == "left":
                    self.direction = (self.direction[0] - int(player.speed / boost_x), self.direction[1])
                elif self.direction[0] < 0 and player.direction == "right":
                    self.direction = (self.direction[0] + int(player.speed / boost_x), self.direction[1])
                elif self.direction[0] < 0 and player.direction == "left":
                    self.direction = (self.direction[0] - int(player.speed / boost_x), self.direction[1])

    def gravity(self):
        # Smaller g = more gravity
        big_g = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
        if self.g % big_g[11] == 0:
            self.direction = (self.direction[0], self.direction[1] + 1)
        if self.g > big_g[11]:
            self.g = 0
        self.g += 1


class MultiBall:

    def __init__(self, direction):
        self.x = int(screen_width / 2)
        self.y = int(screen_height / 5)
        self.radius = 15
        self.direction = direction
        self.g = 0

    def move(self):
        self.clear()
        self.bounce_wall()
        self.bounce_paddle()
        self.bounce_ball()
        self.gravity()
        self.speed_limit()
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.draw()

    def clear(self):
        if collide(self.x, self.y, self.radius, player.x, player.y, player.width):
            pygame.draw.circle(screen, bgColor, (self.x, self.y), self.radius)
            player.draw()
        else:
            pygame.draw.circle(screen, bgColor, (self.x, self.y), self.radius)

    def draw(self):
        pygame.draw.circle(screen, fgColor, (self.x, self.y), self.radius)

    def reset(self):
        self.__init__((random.randint(-3, 3), random.randint(1, 2)))

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def speed_limit(self):
        max_y_speed = 7
        max_x_speed = 5
        if self.direction[0] > max_x_speed:
            self.direction = (max_x_speed, self.direction[1])
        if self.direction[1] > max_y_speed:
            self.direction = (self.direction[0], max_y_speed)

    def bounce_wall(self):
        if self.x <= self.radius:
            self.direction = (-self.direction[0], self.direction[1])
            self.update_pos(self.radius, self.y)
        elif self.x >= screen_width - self.radius:
            self.direction = (-self.direction[0], self.direction[1])
            self.update_pos((screen_width - self.radius), self.y)
        if self.y <= self.radius:
            self.direction = (self.direction[0], -self.direction[1])
            self.update_pos(self.x, self.radius)
        if self.y >= screen_height - self.radius:
            self.reset()

    def bounce_paddle(self):
        # higher number = less boost
        boost_x = 300
        boost_y = 400
        if collide(self.x, self.y, self.radius, player.x, player.y, player.width):
            self.update_pos(self.x, player.y - self.radius)
            self.direction = (self.direction[0], -int(self.direction[1] + player.speed / boost_y))
            if player.direction != "":
                if self.direction[0] >= 0 and player.direction == "right":
                    self.direction = (self.direction[0] + int(player.speed / boost_x), self.direction[1])
                elif self.direction[0] >= 0 and player.direction == "left":
                    self.direction = (self.direction[0] - int(player.speed / boost_x), self.direction[1])
                elif self.direction[0] < 0 and player.direction == "right":
                    self.direction = (self.direction[0] + int(player.speed / boost_x), self.direction[1])
                elif self.direction[0] < 0 and player.direction == "left":
                    self.direction = (self.direction[0] - int(player.speed / boost_x), self.direction[1])

    def bounce_ball(self):
        for i in range(len(multi_ball)):
            if self.x != multi_ball[i].x and self.y != multi_ball[i].y:
                if multi_ball[i].x + multi_ball[i].radius + self.radius >= self.x:
                    if self.x >= multi_ball[i].x - multi_ball[i].radius - self.radius:
                        if multi_ball[i].y + multi_ball[i].radius + self.radius >= self.y:
                            if self.y >= multi_ball[i].y - multi_ball[i].radius - self.radius:
                                multi_ball[i].draw()

    def gravity(self):
        # Smaller g = more gravity
        big_g = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
        if self.g % big_g[11] == 0:
            self.direction = (self.direction[0], self.direction[1] + 1)
        if self.g > big_g[11]:
            self.g = 0
        self.g += 1


class Paddle:

    def __init__(self, x, y, width, height, direction, speed):
        self.x = int(x - width / 2)
        self.y = int(y - height / 2)
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed
        self.boost = False
        self.color = fgColor

    def clear(self):
        pygame.draw.rect(screen, bgColor, (self.x, self.y, self.width, self.height))

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        if self.direction == "left" and self.x >= 0:
            self.clear()
            self.x -= int(self.speed / 100)
            self.draw()
        elif self.direction == "right" and self.x <= screen_width - self.width:
            self.clear()
            self.x += int(self.speed / 100)
            self.draw()


class Brick:
    def __init__(self):
        self.x = ""
        self.y = ""
        self.color = ""


def collide(ball_x, ball_y, ball_r, paddle_x, paddle_y, paddle_w):
    if paddle_x + paddle_w + ball_r >= ball_x >= paddle_x - ball_r and ball_y >= paddle_y - ball_r:
        return True


def cheater_mode():
    player.clear()

    # Follow Ball
    if ball.x < (player.x + player.width / 2) + 1:
        player.direction = "left"
    elif ball.x > (player.x + player.width / 2) - 1:
        player.direction = "right"
    if (player.x + player.width / 2) - 1 <= ball.x <= (player.x + player.width / 2) + 1:
        player.direction = ""

    # Give Ball x Momentum
    if player.direction == "":
        if collide(ball.x, ball.y, ball.radius, player.x, player.y, player.width) and ball.direction[0] == 0:
            ran = random.randint(0, 10)
            if ran % 2 == 0:
                player.direction = "left"
            else:
                player.direction = "right"

    # Teleport to Ball
    if ball.x > player.x + player.width + ball.radius:
        player.clear()
        player.x = ball.x - ball.radius - player.width
        player.draw()
    if ball.x < player.x:
        player.clear()
        player.x = ball.x
        player.draw()
    # Emergency Teleport
    if ball.y + ball.radius >= screen_height - 1:
        if ball.direction[0] >= 0:
            player.x = ball.x - player.width / 2
            player.direction = "right"
        else:
            player.x = ball.x - player.width / 2
            player.direction = "left"

    player.color = (255, 0, 0)
    player.draw()


def cheater_mode_multi():
    player.clear()

    # Follow Ball
    if multi_ball[0].x < (player.x + player.width / 2) + 1:
        player.direction = "left"
    elif multi_ball[0].x > (player.x + player.width / 2) - 1:
        player.direction = "right"
    if (player.x + player.width / 2) - 1 <= multi_ball[0].x <= (player.x + player.width / 2) + 1:
        player.direction = ""

    # Give Ball x Momentum
    if player.direction == "":
        if collide(multi_ball[0].x, multi_ball[0].y, multi_ball[0].radius, player.x, player.y, player.width):
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

    player.color = (255, 0, 0)
    player.draw()


# Initialize Ball
# ball = Ball((0, 1))
# ball.draw()

# Multi-Ball
multi_ball = [0]
ball_m = 1
multi_ball[0] = MultiBall((0, 1))

# Initialize Paddle
player = Paddle(int(screen_width / 2), int(screen_height - (screen_height / 30)), 150, 20, "", 300)
player.draw()

# Initialize Bricks
bricks = Brick()

# Game Loop
clock = pygame.time.Clock()
running = True
cheater = True
pause = False
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
                player.speed += 300
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
                multi_ball.append(ball_m)
                # multi_ball[len(multi_ball) - 1] = Ball((random.randint(-3, 3), random.randint(1, 2)))
                multi_ball[len(multi_ball) - 1] = MultiBall((0, 1))
                ball_m += 1

            # Pause
            if keys[K_SPACE] and pause is False:
                pause = True
            elif keys[K_SPACE] and pause is True:
                pause = False

            # Frame Advance
            if pause is True:
                if cheater:
                    # cheater_mode()
                    cheater_mode_multi()
                if keys[K_n]:
                    player.move()
                    # ball.move()
                    for i in range(len(multi_ball)):
                        multi_ball[i].move()
                    pygame.display.flip()

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
                player.speed -= 300
                player.boost = False
    if cheater:
        # cheater_mode()
        cheater_mode_multi()
    if pause is False:
        player.move()
        # ball.move()
        for i in range(len(multi_ball)):
            multi_ball[i].move()
        pygame.display.flip()
    clock.tick(240)
