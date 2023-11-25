import pygame
import random
pygame.init()

CELL_SIZE = 5
CELL_BORDER = 1+CELL_SIZE//10

WIDTH = 1400+CELL_BORDER
HEIGHT = 750+CELL_BORDER

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("random walker")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (190, 190, 190)

FPS = 60

cells = {}
path = set()
cells_rows = WIDTH//CELL_SIZE
cells_cols = HEIGHT//CELL_SIZE
starting_cell = (cells_rows//2, cells_cols//2)
path.add(starting_cell)


def set_starting_board():
    DISPLAY.fill(BLACK)
    i = 0
    for x in range(CELL_BORDER, WIDTH, CELL_SIZE):
        j = 0
        for y in range(CELL_BORDER, HEIGHT, CELL_SIZE):
            cell = pygame.Rect(x, y, CELL_SIZE-CELL_BORDER,
                               CELL_SIZE-CELL_BORDER)
            pygame.draw.rect(DISPLAY, LIGHTGRAY, cell)

            cells[(i, j)] = cell
            j += 1
        i += 1

    pygame.display.update()


def walk():
    global starting_cell

    a = starting_cell[0]
    b = starting_cell[1]

    chance = random.randint(1, 4)
    x = 0
    y = 0

    if chance == 1:
        if a < cells_rows-1:
            x += 1
    elif chance == 2:
        if a > 0:
            x -= 1
    elif chance == 3:
        if b < cells_cols-1:
            y += 1
    else:
        if b > 0:
            y -= 1

    a += x
    b += y

    starting_cell = (a, b)
    path.add(starting_cell)


def display():

    for cords, cell in cells.items():
        if cords in path:
            color = BLACK
        else:
            color = LIGHTGRAY
        pygame.draw.rect(DISPLAY, color, cell)

    pygame.display.update()


def main():

    run = True

    clock = pygame.time.Clock()

    set_starting_board()

    stamp = 5
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for _ in range(stamp):
            walk()
            display()


if __name__ == "__main__":
    main()
    pygame.quit()
    quit()
