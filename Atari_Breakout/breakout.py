import pygame
from random import randint
from math import sqrt
from os import system
pygame.init()


class Window:
    """
        The class for operating the game window.
    """

    def __init__(self, width, height, window_name, max_fps):
        self.width = width
        self.height = height
        self.max_fps = max_fps
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(window_name)

    def fill(self, color):
        """
            Fill the background with one color.
        """
        self.window.fill(color)

    def update(self):
        """
            Updates the display.
        """
        pygame.display.update()


class Colors:
    """
        A class storing all the game colors.
    """

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    orange = (255, 165, 0)
    yellow = (255, 255, 0)

    background_color = black
    paddle_color = blue
    ball_color = white
    obstacle_color = green

# TODO: dodac zmniejszanie paletki


class Paddle:
    """
        A class for operating bottom paddle.
    """

    def __init__(self, width, height, color, speed, window):
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.window = window
        self.body = pygame.Rect((self.window.width-self.width)//2,
                                self.window.height-self.height, self.width, self.height)

    def display(self):
        pygame.draw.rect(self.window.window, self.color, self.body)

    def move(self, controls):
        if controls:
            left_border = False
            right_border = False
            key_pressed = pygame.key.get_pressed()

            if self.body.x <= 0:
                left_border = True

            elif self.body.x + self.width >= self.window.width:
                right_border = True

            if (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]) and (key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]):
                return

            elif not right_border and (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]):
                self.body.x += self.speed

            elif not left_border and (key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]):
                self.body.x -= self.speed

        else:
            mouse_pos = pygame.mouse.get_pos()
            self.body.x = mouse_pos[0] - self.body.width//2


class Ball(Paddle):
    def __init__(self, size, color, speed, window):
        self.size = size
        self.color = color
        self.xspeed = speed
        self.yspeed = speed
        self.net = sqrt((self.xspeed)**2+(self.yspeed)**2)  # const ~ 9.9
        self.window = window
        self.hit_counter = 0
        self.starting_x = (self.window.width-self.size)//2
        self.starting_y = (self.window.height-self.size)//2
        self.bounce = [speed/4, speed/3, speed/2, speed]
        self.body = pygame.Rect(
            self.starting_x, self.starting_y, self.size, self.size)

    def move(self):
        """
            Function that moves the Ball.
        """
        self.body.y += self.yspeed
        self.body.x += self.xspeed

    def check_collisions(self, paddle, obstacles):

        # horizontal collision
        if self.body.x <= 0 or self.body.x + self.size >= self.window.width:
            self.xspeed *= -1

        # paddle collision
        if self.body.colliderect(paddle.body):
            self.xspeed *= -1
            self.yspeed *= -1

        # loose checker
        elif self.body.y + self.size >= self.window.height:
            self.body.x = self.starting_x
            self.body.y = self.starting_y
            return

        # vertical collision
        elif self.body.y <= 0:
            self.yspeed *= -1

        # __________________________
        for obstacle in obstacles:

            if self.body.colliderect(obstacle.body):
                if self.hit_counter == 3 or self.hit_counter == 11:
                    if self.yspeed > 0:
                        self.yspeed += 0.5
                    else:
                        self.yspeed -= 0.5

                    if self.xspeed > 0:
                        self.xspeed += 1
                    else:
                        self.xspeed -= 1

                self.xspeed *= -1
                self.yspeed *= -1

                obstacles.remove(obstacle)

                self.hit_counter += 1


class Obstacle(Ball):
    def __init__(self, x, y, width, height, color, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.window = window
        self.body = pygame.Rect(
            self.x, self.y, self.width, self.height)

    def display(self):
        pygame.draw.rect(self.window.window, self.color, self.body)


def clear():
    system('clear')


def create_obstacles(row, column, window, colors):
    obstacles = []
    obs_width = 36
    obs_height = 20
    margin = 3
    #top = 100

    for y in range(column):
        for x in range(row):
            obs_x = x * obs_width
            obs_y = y * obs_height

            if y == 0 or y == 1:
                color = colors.red
            elif y == 2 or y == 3:
                color = colors.orange
            elif y == 4 or y == 5:
                color = colors.green
            else:
                color = colors.yellow
            obstacle = Obstacle(obs_x, obs_y, obs_width-margin,
                                obs_height-margin, color, window)
            obstacles.append(obstacle)

    return obstacles


def main():

    clear()

    run = True
    controls = True

    clock = pygame.time.Clock()
    window = Window(502, 800, "Breakout", 60)
    colors = Colors()
    paddle = Paddle(50, 20, colors.paddle_color, 7, window)
    ball = Ball(10, colors.ball_color, 5, window)
    obstacles = create_obstacles(14, 8, window, colors)

    window.fill(colors.black)
    paddle.display()
    ball.display()

    for obstacle in obstacles:
        obstacle.display()

    window.update()

    while run:

        clock.tick(window.max_fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    controls = not controls

        ball.check_collisions(paddle, obstacles)
        paddle.move(controls)
        ball.move()
        window.fill(colors.background_color)
        paddle.display()
        ball.display()

        for obstacle in obstacles:
            obstacle.display()

        window.update()


if __name__ == "__main__":
    main()
    pygame.quit()
    exit()
