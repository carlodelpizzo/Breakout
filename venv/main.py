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


class MultiBall:

    def __init__(self, direction):
        self.x = int(screen_width / 2)
        self.y = int(screen_height / 5)
        self.radius = 15
        self.direction = direction
        self.g = 0

    def move(self):
        self.bounce_wall()
        self.bounce_paddle()
        self.gravity()
        self.speed_limit()
        if self.collide_ball() is False:
            self.x += self.direction[0]
            self.y += self.direction[1]
        else:
            self.x += self.direction[0]
            self.y += self.direction[1]

    def clear(self):
        if self.collide_paddle(player.x, player.y, player.width):
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
        if self.collide_paddle(player.x, player.y, player.width):
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

    def collide_paddle(self, paddle_x, paddle_y, paddle_w):
        if paddle_x + paddle_w + self.radius >= self.x >= paddle_x - self.radius and self.y >= paddle_y - self.radius:
            return True

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
            self.x -= int(self.speed / 100)
        elif self.direction == "right" and self.x <= screen_width - self.width:
            self.x += int(self.speed / 100)


class Brick:
    def __init__(self):
        self.x = ""
        self.y = ""
        self.color = ""


def cheater_mode():
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

    player.color = (255, 0, 0)
    player.draw()


# Initialize Ball (direction)
multi_ball = [0]
ball_m = 1
multi_ball[0] = MultiBall((0, 1))

# Initialize Paddle (x, y, width, height, direction, speed)
player = Paddle(int(screen_width / 2), int(screen_height - (screen_height / 30)), 200, 20, "", 300)
player.draw()

# Initialize Bricks
bricks = Brick()

# Game Loop
clock = pygame.time.Clock()
running = True
cheater = False
pause = False


def game_loop():
    if cheater:
        cheater_mode()
    player.clear()
    player.move()
    player.draw()
    for i in range(len(multi_ball)):
        multi_ball[i].clear()
        multi_ball[i].move()
    for i in range(len(multi_ball)):
        multi_ball[i].draw()
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
                player.speed -= 300
                player.boost = False

    if pause is False:
        game_loop()
    clock.tick(240)
