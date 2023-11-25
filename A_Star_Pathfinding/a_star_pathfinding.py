import pygame
from os import system
from math import sqrt

pygame.init()

CELL_SIZE = 20
BORDER_WIDTH = CELL_SIZE//20

# window setup
WIDTH = 1000+BORDER_WIDTH
HEIGHT = 600+BORDER_WIDTH
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("a* algo")

ROW_SIZE = WIDTH//CELL_SIZE
COL_SIZE = HEIGHT//CELL_SIZE

CORDS_FONT = pygame.font.SysFont("comicsans", CELL_SIZE//4)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)

BORDER_COLOR = BLACK

borders = {}
cells = {}

starting_cell = []
ending_cell = []
obstacles = []

open = {}
closed = []


FPS = 60


def clear():
    system('clear')


def set_starting_grid():
    for y in range(0, HEIGHT, CELL_SIZE):
        for x in range(0, WIDTH, CELL_SIZE):

            col_id = x//CELL_SIZE
            row_id = y//CELL_SIZE

            border = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            borders[(col_id, row_id)] = border

            cell = pygame.Rect(x+BORDER_WIDTH, y+BORDER_WIDTH,
                               CELL_SIZE-BORDER_WIDTH, CELL_SIZE-BORDER_WIDTH)
            cells[(col_id, row_id)] = cell


def draw_grid():
    for border in borders.values():
        pygame.draw.rect(DISPLAY, BORDER_COLOR, border, BORDER_WIDTH)

    for key, cell in cells.items():
        if key in starting_cell:
            cell_color = LIGHT_BLUE
            pygame.draw.rect(DISPLAY, cell_color, cell)
            a_text = CORDS_FONT.render("A", 1, BLACK)
            DISPLAY.blit(a_text,
                         (cell.x + CELL_SIZE//2 - a_text.get_width()//2,
                          cell.y + CELL_SIZE//2 - a_text.get_height()//2))
        elif key in ending_cell:
            cell_color = LIGHT_BLUE
            pygame.draw.rect(DISPLAY, cell_color, cell)
            b_text = CORDS_FONT.render("B", 1, BLACK)
            DISPLAY.blit(b_text,
                         (cell.x + CELL_SIZE//2 - b_text.get_width()//2,
                          cell.y + CELL_SIZE//2 - b_text.get_height()//2))
        elif key in obstacles:
            cell_color = BLACK
            pygame.draw.rect(DISPLAY, cell_color, cell)

        elif key in list(open.keys()):
            cell_color = GREEN
            pygame.draw.rect(DISPLAY, cell_color, cell)
            f_cost = str(round(open[key], 2))
            f_cost_text = CORDS_FONT.render(f_cost, 1, BLACK)
            DISPLAY.blit(f_cost_text,
                         (cell.x + CELL_SIZE//2 - f_cost_text.get_width()//2,
                          cell.y + CELL_SIZE//2 - f_cost_text.get_height()//2))
        elif key in closed:
            cell_color = RED
            pygame.draw.rect(DISPLAY, cell_color, cell)
        else:
            cell_color = WHITE
            pygame.draw.rect(DISPLAY, cell_color, cell)

    pygame.display.update()


def pick_starting_cell():
    global picking_starting_cell

    starting_cell.clear()

    mouse_x_pos = pygame.mouse.get_pos()[0]
    mouse_y_pos = pygame.mouse.get_pos()[1]

    clicked_cell = (mouse_x_pos//CELL_SIZE, mouse_y_pos//CELL_SIZE)

    if clicked_cell not in ending_cell:
        starting_cell.append(clicked_cell)
        print(f"starting cell picked - {clicked_cell}")
        picking_starting_cell = False


def pick_ending_cell():
    global picking_ending_cell

    ending_cell.clear()

    mouse_x_pos = pygame.mouse.get_pos()[0]
    mouse_y_pos = pygame.mouse.get_pos()[1]

    clicked_cell = (mouse_x_pos//CELL_SIZE, mouse_y_pos//CELL_SIZE)

    if clicked_cell not in starting_cell:
        ending_cell.append(clicked_cell)
        print(f"ending cell picked - {clicked_cell}")
        picking_ending_cell = False


def draw_obstacles():
    global drawing_obstacles

    mouse_x_pos = pygame.mouse.get_pos()[0]
    mouse_y_pos = pygame.mouse.get_pos()[1]

    clicked_cell = (mouse_x_pos//CELL_SIZE, mouse_y_pos//CELL_SIZE)

    if clicked_cell not in starting_cell and clicked_cell not in ending_cell and clicked_cell not in obstacles:
        obstacles.append(clicked_cell)


def a_star_algo(time):
    global start_algo
    key_pressed = pygame.key.get_pressed()

    if time % 1 != 0:
        return

    starting = starting_cell[0]
    ending = ending_cell[0]
    all_keys = list(borders.keys())
    min_f_cost = 1000000000

    for cell, f_cost in open.items():

        if f_cost < min_f_cost:
            min_f_cost = f_cost
            current = cell

    del open[current]
    closed.append(current)

    if current == ending:
        print("done")
        start_algo = False
        return

    # checking neighbours of the current
    for y in range(-1, 2):
        for x in range(-1, 2):

            neigh_x = current[0]+x
            neigh_y = current[1]+y
            neigh = (neigh_x, neigh_y)

            if neigh not in all_keys or neigh in closed or neigh in obstacles:
                continue

            keys = list(open.keys())

            if neigh not in keys:
                g_cost = sqrt(
                    (neigh[0]-starting[0])**2 + (neigh[1]-starting[1])**2)
                h_cost = sqrt(
                    (neigh[0]-ending[0])**2 + (neigh[1]-ending[1])**2)
                f_cost = g_cost + h_cost
                open[neigh] = f_cost


def main():
    global picking_starting_cell
    global picking_ending_cell
    global drawing_obstacles
    global start_algo

    # global data setup
    borders.clear()
    cells.clear()
    obstacles.clear()
    starting_cell.clear()
    ending_cell.clear()
    open.clear()
    closed.clear()

    picking_starting_cell = False
    picking_ending_cell = False
    drawing_obstacles = False
    start_algo = False

    # loop setup
    run = True
    clock = pygame.time.Clock()
    time = 0

    # grid setup
    set_starting_grid()
    draw_grid()

    # animation loop
    while run:
        clock.tick(FPS)

        time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type != pygame.KEYDOWN:
                continue

            # reset
            elif event.key == pygame.K_r:
                print("reset")
                main()

            elif event.key == pygame.K_s:
                open.clear()
                closed.clear()

            # obstacles clear
            elif event.key == pygame.K_c and not start_algo:
                print("clearing path")
                obstacles.clear()

            # picking starting cell
            elif event.key == pygame.K_1 and not start_algo:
                print("choosing starting cell")
                picking_ending_cell = False
                drawing_obstacles = False
                picking_starting_cell = True

            # picking ending cell
            elif event.key == pygame.K_2 and not start_algo:
                print("choosing ending cell")
                picking_starting_cell = False
                drawing_obstacles = False
                picking_ending_cell = True

            # drawing obstacles
            elif event.key == pygame.K_3 and not start_algo:
                print("drawing obstacles")
                picking_starting_cell = False
                picking_ending_cell = False
                drawing_obstacles = True

            elif event.key == pygame.K_SPACE:
                print("starting the algo\n\n")
                picking_starting_cell = False
                picking_ending_cell = False
                drawing_obstacles = False
                start_algo = True
                starting = starting_cell[0]
                ending = ending_cell[0]
                f_cost = sqrt((starting[0]**2-ending[0]) **
                              2+(starting[1]-ending[1])**2)
                open[starting] = f_cost

        LMB_is_clicked = pygame.mouse.get_pressed()[0]

        if picking_starting_cell and LMB_is_clicked:
            pick_starting_cell()

        if picking_ending_cell and LMB_is_clicked:
            pick_ending_cell()

        if drawing_obstacles and LMB_is_clicked:
            draw_obstacles()

        if start_algo and starting_cell and ending_cell:
            a_star_algo(time)

        if starting_cell or ending_cell or obstacles:
            draw_grid()

    # exit
    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
