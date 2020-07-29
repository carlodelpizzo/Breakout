import pygame
import random
import math
from pygame.locals import *

pygame.init()

# Initialize Screen
screenWidth = 1000
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
# Title
pygame.display.set_caption("Title")
# Set Screen Colors
bgColor = [0, 0, 0]
fgColor = [50, 100, 200]


class Ball:

    def __init__(self, direction):
        self.xPos = int(screenWidth / 2)
        self.yPos = int(screenHeight / 5)
        self.radius = 15
        self.direction = direction

    def clear(self):
        if collide(self.xPos, self.yPos, self.radius, player.xPos, player.yPos, player.width):
            pygame.draw.circle(screen, bgColor, (self.xPos, self.yPos), self.radius)
            player.draw()
        else:
            pygame.draw.circle(screen, bgColor, (self.xPos, self.yPos), self.radius)

    def draw(self):
        pygame.draw.circle(screen, fgColor, (self.xPos, self.yPos), self.radius)

    def move(self):
        self.bounce_wall()
        self.bounce_paddle()
        self.clear()
        if self.direction[0] > 10:
            self.direction = (11 - (self.direction[0] % 10), self.direction[1])
            self.xPos += self.direction[0]
        else:
            self.xPos += self.direction[0]
        if self.direction[1] > 10:
            self.direction = (self.direction[0], 11 - (self.direction[1] % 10))
        else:
            self.yPos += self.direction[1]
        self.draw()

    def flip_x(self):
        self.direction = (-self.direction[0], self.direction[1])

    def flip_y(self):
        self.direction = (self.direction[0], -self.direction[1])

    def update_pos(self, x, y):
        self.clear()
        self.xPos = x
        self.yPos = y
        self.draw()

    def bounce_wall(self):
        if self.xPos <= self.radius:
            self.flip_x()
            self.update_pos(self.radius, self.yPos)
        elif self.xPos >= screenWidth - self.radius:
            self.flip_x()
            self.update_pos((screenWidth - self.radius), self.yPos)
        if self.yPos <= self.radius:
            self.flip_y()
            self.update_pos(self.xPos, self.radius)
        if self.yPos >= screenHeight - self.radius:
            self.reset()

    def bounce_paddle(self):
        boost_x = 300
        boost_y = 500
        if collide(self.xPos, self.yPos, self.radius, player.xPos, player.yPos, player.width):
            self.update_pos(self.xPos, player.yPos - self.radius)
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

    def reset(self):
        self.clear()
        self.__init__((random.randint(-3, 3), random.randint(1, 2)))


class Paddle:

    def __init__(self, x, y, width, height, direction, speed):
        self.xPos = int(x - width / 2)
        self.yPos = int(y - height / 2)
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed
        self.boost = False
        self.color = fgColor

    def clear(self):
        pygame.draw.rect(screen, bgColor, (self.xPos, self.yPos, self.width, self.height))

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.xPos, self.yPos, self.width, self.height))

    def move(self):
        if self.direction == "left" and self.xPos >= 0:
            self.clear()
            self.xPos -= int(self.speed / 100)
            self.draw()
        elif self.direction == "right" and self.xPos <= screenWidth - self.width:
            self.clear()
            self.xPos += int(self.speed / 100)
            self.draw()


class Brick:
    def __init__(self):
        self.xPos = ""
        self.yPos = ""
        self.color = ""


def collide(ball_x, ball_y, ball_r, paddle_x, paddle_y, paddle_w):
    if paddle_x + paddle_w + ball_r >= ball_x >= paddle_x - ball_r and ball_y >= paddle_y - ball_r:
        return True


def cheater_mode():
    player.clear()
    if ball.xPos < (player.xPos + player.width / 2) + 1:
        player.direction = "left"
    elif ball.xPos > (player.xPos + player.width / 2) - 1:
        player.direction = "right"
    if (player.xPos + player.width / 2) - 1 <= ball.xPos <= (player.xPos + player.width / 2) + 1:
        player.direction = ""
    if ball.yPos + ball.radius >= player.yPos - 3:
        if ball.direction[0] >= 0:
            player.xPos = ball.xPos - player.width / 2
            player.direction = "right"
        else:
            player.xPos = ball.xPos - player.width / 2
            player.direction = "left"
    player.color = (255, 0, 0)
    player.draw()


# Initialize Ball
ball = Ball((0, 1))
ball.draw()
# Initialize Paddle
player = Paddle(int(screenWidth / 2), int(screenHeight - (screenHeight / 30)), 150, 20, "", 300)
player.draw()
# Initialize Bricks
bricks = Brick()

clock = pygame.time.Clock()
running = True
cheater = False
# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        # On Key Down
        if event.type == pygame.KEYDOWN:
            # Left/Right Movement
            if keys[pygame.K_LEFT]:
                if keys[pygame.K_RIGHT]:
                    player.direction = ""
                else:
                    player.direction = "left"
            elif keys[pygame.K_RIGHT]:
                if keys[pygame.K_LEFT]:
                    player.direction = ""
                else:
                    player.direction = "right"

            # Shift Boost
            if keys[K_LSHIFT] and player.boost is False:
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

        # On Key Up
        if event.type == pygame.KEYUP:
            # Left/Right Movement
            if player.direction == "left" and keys[pygame.K_LEFT] == 0:
                player.direction = ""
            elif player.direction == "right" and keys[pygame.K_RIGHT] == 0:
                player.direction = ""
            elif keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] == 0:
                player.direction = "left"
            elif keys[pygame.K_RIGHT] and keys[pygame.K_LEFT] == 0:
                player.direction = "right"

            # Shift Boost
            if keys[K_LSHIFT] == 0 and player.boost is True:
                player.speed -= 300
                player.boost = False

    if cheater:
        cheater_mode()
    player.move()
    ball.move()
    pygame.display.flip()
    clock.tick(240)
