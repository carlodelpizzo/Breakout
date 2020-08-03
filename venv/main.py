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
red = [255, 0, 0]
blue = [0, 255, 0]
green = [0, 0, 255]
white = [255, 255, 255]
# Font
font_size = 25
font_face = "Calibri"
font = pygame.font.SysFont(font_face, 25)


class MultiBall:

    def __init__(self, direction):
        self.radius = 11
        self.x = screen_width / 2
        if len(bricks) != 0:
            self.y = bricks[len(bricks) - 1].y + bricks[len(bricks) - 1].height + self.radius + 1
        else:
            self.y = screen_height / 2
        self.direction = direction
        self.g = 0
        self.color = fgColor
        self.max_x = 4
        self.max_y = 5
        self.influence = False
        self.i = 0

    def move(self):
        # self.gravity()
        self.bounce_wall()
        self.bounce_paddle()
        self.bounce_brick()
        self.update_pos(self.x + self.speed_limit_x(self.direction[0]), self.y + self.speed_limit_y(self.direction[1]))

    def clear(self):
        if self.collide_paddle(player.x, player.y, player.width):
            pygame.draw.circle(screen, bgColor, (int(self.x), int(self.y)), self.radius)
            player.draw()
        else:
            pygame.draw.circle(screen, bgColor, (int(self.x), int(self.y)), self.radius)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def speed_limit_x(self, x_dir):
        if self.direction[0] > self.max_x:
            limited_x = self.max_x
        elif self.direction[0] < -self.max_x:
            limited_x = -self.max_x
        else:
            limited_x = x_dir
        return limited_x

    def speed_limit_y(self, y_dir):
        if self.direction[1] > self.max_y:
            limited_y = self.max_y
        elif self.direction[1] < -self.max_y:
            limited_y = -self.max_y
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
            i = self.i
            self.__init__((0, 1))
            self.i = i

    def bounce_paddle(self):
        boost_x = (1 / player.speed) * 1.1
        boost_y = (1 / player.speed) * 1
        if player.boost:
            boost_x *= 4
            boost_y *= 4

        if self.collide_paddle(player.x, player.y, player.width):
            player.influence[self.i] = (int(frame_rate / 5))
            self.influence = True
            self.update_pos(self.x, player.y - self.radius)
            if player.direction != "":
                # if ball direction == right
                if self.direction[0] > 0:
                    if player.direction == "right":
                        self.direction = (self.direction[0] + self.direction[0] * boost_x,
                                          -self.direction[1] - self.direction[1] * boost_y)
                    elif player.direction == "left":
                        self.direction = (self.direction[0] - self.direction[0] * boost_x,
                                          -self.direction[1] + self.direction[1] * boost_y)
                # if ball direction == left
                elif self.direction[0] < 0:
                    if player.direction == "right":
                        self.direction = (self.direction[0] + abs(self.direction[0]) * boost_x,
                                          -self.direction[1] + self.direction[1] * boost_y)
                    elif player.direction == "left":
                        self.direction = (self.direction[0] - abs(self.direction[0]) * boost_x,
                                          -self.direction[1] - self.direction[1] * boost_y)
                # if bal direction == straight
                elif self.direction[0] == 0:
                    if player.direction == "right":
                        self.direction = (self.direction[0] + boost_x + 1,
                                          -self.direction[1] - self.direction[1] * boost_y)
                    elif player.direction == "left":
                        self.direction = (self.direction[0] - boost_x - 1,
                                          -self.direction[1] - self.direction[1] * boost_y)
            elif player.direction == "":
                self.direction = (self.direction[0], -self.direction[1])

        elif self.influence and player.influence[self.i] > 0:
            if player.direction == "right":
                player.influence[self.i] = 0
                self.influence = False
                # Ball direction == right
                if self.direction[0] > 0:
                    self.direction = (self.direction[0] + self.direction[0] * boost_x,
                                      self.direction[1] + self.direction[1] * boost_y)
                # Ball direction == left
                elif self.direction[0] < 0:
                    self.direction = (self.direction[0] + abs(self.direction[0]) * boost_x,
                                      self.direction[1] - self.direction[1] * boost_y)
                # Ball direction == straight
                elif self.direction[0] == 0:
                    self.direction = (self.direction[0] + boost_x + 1,
                                      self.direction[1] + self.direction[1] * boost_y)
            elif player.direction == "left":
                player.influence[self.i] = 0
                self.influence = False
                # Ball direction == right
                if self.direction[0] > 0:
                    self.direction = (self.direction[0] - self.direction[0] * boost_x,
                                      self.direction[1] - self.direction[1] * boost_y)
                # Ball direction == left
                elif self.direction[0] < 0:
                    self.direction = (self.direction[0] - abs(self.direction[0]) * boost_x,
                                      self.direction[1] + self.direction[1] * boost_y)
                # Ball direction == straight
                elif self.direction[0] == 0:
                    self.direction = (self.direction[0] - boost_x - 1,
                                      self.direction[1] + self.direction[1] * boost_y)

        if player.boost:
            boost_x /= 4
            boost_y /= 4

    def collide_paddle(self, paddle_x, paddle_y, paddle_w):
        if paddle_x + paddle_w + self.radius >= self.x >= paddle_x - self.radius and self.y >= paddle_y - self.radius:
            self.direction = (self.speed_limit_x(self.direction[0]), self.speed_limit_y(self.direction[1]))
            return True
        else:
            return False

    def bounce_brick(self):
        for brick in range(len(bricks)):
            if bricks[brick].x + bricks[brick].width + self.radius >= self.x >= bricks[brick].x - self.radius:
                if bricks[brick].y - self.radius <= self.y <= bricks[brick].y + bricks[brick].height + self.radius:
                    # Is Ball within center region of Brick
                    if bricks[brick].x + bricks[brick].width - 1 > self.x > bricks[brick].x + 1:
                        # Closer to bottom than top of Brick
                        if self.y - self.radius - bricks[brick].y + bricks[brick].height > \
                                bricks[brick].y - self.y + self.radius:
                            self.y = bricks[brick].y + bricks[brick].height + self.radius + 1
                            self.direction = (self.direction[0], -self.direction[1])
                        else:
                            self.y = bricks[brick].y - self.radius - 1
                            self.direction = (self.direction[0], -self.direction[1])
                    else:
                        # Closer to left than right of Brick
                        if self.x - bricks[brick].x < bricks[brick].x + bricks[brick].width - self.x:
                            self.x = bricks[brick].x - self.radius - 1
                            self.direction = (-self.direction[0], self.direction[1])
                        else:
                            self.x = bricks[brick].x + bricks[brick].width + self.radius + 1
                            self.direction = (-self.direction[0], self.direction[1])

                    # Break Brick or Lower Brick Level
                    if bricks[brick].cooldown == 0:
                        if bricks[brick].level - 1 == 0:
                            bricks.pop(brick)
                        else:
                            bricks[brick].level -= 1
                            bricks[brick].color = brick_colors[(bricks[brick].level % len(brick_colors))]
                            bricks[brick].cooldown = int(frame_rate / 10)
                    break

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

    def __init__(self, width, height, speed):
        self.x = screen_width / 2 - width / 2
        self.y = screen_height - (screen_height / 30) - height / 2
        self.width = width
        self.height = height
        self.direction = ""
        self.speed = speed
        self.boost = False
        self.color = fgColor
        self.influence = [0]

    def move(self):
        if self.direction == "left" and self.x >= 0:
            self.x -= int(self.speed)
        elif self.direction == "right" and self.x <= screen_width - self.width:
            self.x += int(self.speed)

        self.inf_drain()

    def clear(self):
        pygame.draw.rect(screen, bgColor, (int(self.x), int(self.y), self.width, self.height))

    def draw(self):
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.width, self.height))

    def inf_drain(self):
        for i in range(len(self.influence)):
            if self.influence[i] > 1:
                self.influence[i] -= 1
            elif self.influence[i] == 1:
                self.influence[i] -= 1
                multi_ball[i].influence = False


class Brick:
    def __init__(self, x, y, width, height, level):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = fgColor
        self.level = level
        self.cooldown = 0

    def draw(self):
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), int(self.width), int(self.height)))

    def clear(self):
        pygame.draw.rect(screen, bgColor, (int(self.x), int(self.y), self.width, self.height))

    def drain_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1


# Initialize Bricks (x, y, width, height, level)
# brick colors to indicate break level
brick_colors = [fgColor, red, green, blue]
bricks = []


def init_bricks():
    brick_col = 6
    brick_row = 3
    brick_lvl = 2
    brick_w = (screen_width / brick_col) * 0.70
    brick_h = 20
    brick_space = (screen_width / brick_col - brick_w) * brick_col / (brick_col + 1)
    for row in range(brick_row):
        for col in range(brick_col):
            bricks.append((row * brick_col) + col)
            x_offset = brick_space + (brick_w + brick_space) * col
            y_offset = brick_space + (brick_h + brick_space) * row
            bricks[(row * brick_col) + col] = Brick(x_offset, y_offset, brick_w, brick_h, brick_lvl)


init_bricks()


# Initialize Ball (direction)
multi_ball = [0]
multi_ball[0] = MultiBall((0, 1))

# Initialize Paddle (x, y, width, height, direction, speed)
player = Player(200, 20, 3)
shift_boost = player.speed * 2
player.draw()

# Game Loop
clock = pygame.time.Clock()
running = True
cheater = False
pause = False
stats = False
frame_rate = 144


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
    for brick in range(len(bricks)):
        bricks[brick].draw()
        bricks[brick].drain_cooldown()

    # Ball
    for i in range(len(multi_ball)):
        multi_ball[i].move()
    for i in range(len(multi_ball)):
        multi_ball[i].draw()

    # Cheater Mode Stop
    if cheater:
        player.direction = ""

    if stats:
        display_stats()

    pygame.display.flip()


def display_stats():
    stat_num = 0
    # Main Ball Stats
    g_text = str(multi_ball[0].g)
    dx_text = str(multi_ball[0].direction[0])
    dy_text = str(multi_ball[0].direction[1])
    inf_text = str(multi_ball[0].influence)

    display_g = font.render("ball g: " + g_text[0:5], True, white)
    display_inf = font.render("ball inf: " + inf_text, True, white)
    if multi_ball[0].direction[0] >= 0:
        display_dx = font.render("ball x:  " + dx_text[0:5], True, white)
    else:
        display_dx = font.render("ball x: " + dx_text[0:6], True, white)
    if multi_ball[0].direction[1] >= 0:
        display_dy = font.render("ball y: " + dy_text[0:5], True, white)
    else:
        display_dy = font.render("ball y: " + dy_text[0:6], True, white)

    screen.blit(display_g, (0, stat_num))
    stat_num += 1
    screen.blit(display_dx, (0, font_size * stat_num))
    stat_num += 1
    screen.blit(display_dy, (0, font_size * stat_num))
    stat_num += 1
    screen.blit(display_inf, (0, font_size * stat_num))
    stat_num += 1

    # Player Stats
    influence = str(player.influence)
    display_inf = font.render("player inf: " + influence, True, white)
    screen.blit(display_inf, (0, font_size * stat_num))
    stat_num += 1

    # Brick Stats
    display_cool = []
    shown = 0
    for brick in range(len(bricks)):
        if bricks[brick].cooldown != 0:
            cool = str(bricks[brick].cooldown)
            display_cool.append(brick)
            display_cool[shown] = font.render("brick [" + str(brick) + "]: " + cool, True, white)
            screen.blit(display_cool[shown], (0, font_size * stat_num))
            stat_num += 1
            shown += 1
        if bricks[brick].cooldown == 0 and brick in display_cool:
            display_cool.pop(display_cool.index(brick))
            stat_num -= 1
            shown -= 1


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
                multi_ball.append(len(multi_ball) + 1)
                multi_ball[len(multi_ball) - 1] = MultiBall((0, 1))
                player.influence.append(0)
                multi_ball[len(multi_ball) - 1].i = len(multi_ball) - 1

            # Kill Ball
            if keys[K_k]:
                if len(multi_ball) > 1:
                    player.influence.pop(len(multi_ball) - 1)
                    multi_ball.pop(len(multi_ball) - 1)

            # Pause
            if keys[K_SPACE] and pause is False:
                pause = True
            elif keys[K_SPACE] and pause is True:
                pause = False

            # Frame Advance
            if pause is True:
                if keys[K_n]:
                    game_loop()

            # Show Ball Stats
            if keys[K_s] and stats:
                stats = False
            elif keys[K_s]:
                stats = True

            # Reset Game
            if keys[K_r]:
                multi_ball[0].__init__((0, 1))
                bricks = []
                init_bricks()

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
