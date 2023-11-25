import pygame
import random

pygame.init()

# window setup
WIDTH = 1002
HEIGHT = 606
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of life")

# fps limit
FPS = 60

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# how much "alive" cells you wanna start with
STARTING_ALIVE_CELLS = 1000

# map of rect + map of aliveness (bool)
MAP_OF_RECTS = [['0' for x in range(91)] for y in range(55)]


def set_starting_grid(map_of_aliveness):
    col = 0
    for x in range(1, HEIGHT, 11):
        row = 0
        for y in range(1, WIDTH, 11):
            MAP_OF_RECTS[col][row] = pygame.Rect(y, x, 10, 10)
            map_of_aliveness[col][row] = False
            row += 1
        col += 1


def set_starting_alive_cells(map_of_aliveness):
    for _ in range(STARTING_ALIVE_CELLS):
        random_x = random.randint(0, 54)
        random_y = random.randint(0, 90)
        while map_of_aliveness[random_x][random_y] == True:
            random_x = random.randint(0, 54)
            random_y = random.randint(0, 90)
        map_of_aliveness[random_x][random_y] = True


def draw_grid(map_of_aliveness):
    for x in range(55):
        for y in range(91):
            if map_of_aliveness[x][y] == True:
                color = BLACK
            else:
                color = WHITE
            rect = MAP_OF_RECTS[x][y]
            pygame.draw.rect(WIN, color, rect)


def handle_next_gen(map_of_aliveness):
    new_map_of_aliveness = [['0' for x in range(91)] for y in range(55)]

    for x in range(55):
        for y in range(91):
            alive_counter = count_alive_neighbours(
                x, y, map_of_aliveness)
            new_map_of_aliveness[x][y] = change_aliveness(
                x, y, map_of_aliveness, alive_counter)

            # if x == 54:
            #     alive_counter = count_alive_neighbours_right(
            #         x, y, map_of_aliveness)
            #     new_map_of_aliveness[x][y] = change_aliveness(
            #         x, y, map_of_aliveness, alive_counter)

            # elif y == 0:
            #     alive_counter = count_alive_neighbours_top(
            #         x, y, map_of_aliveness)
            #     new_map_of_aliveness[x][y] = change_aliveness(
            #         x, y, map_of_aliveness, alive_counter)

            # elif y == 90:
            #     alive_counter = count_alive_neighbours_bottom(
            #         x, y, map_of_aliveness)
            #     new_map_of_aliveness[x][y] = change_aliveness(
            #         x, y, map_of_aliveness, alive_counter)

            # else:
            #     alive_counter = count_alive_neighbours_inside(
            #         x, y, map_of_aliveness)
            #     new_map_of_aliveness[x][y] = change_aliveness(
            #         x, y, map_of_aliveness, alive_counter)

    return(new_map_of_aliveness)


def count_alive_neighbours(x, y, map_of_aliveness):
    counter = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i == x and j == y:
                continue

            try:
                if map_of_aliveness[i][j] == True:
                    counter += 1

            except:
                continue

    return counter


def change_aliveness(x, y, map_of_aliveness, alive_counter):
    if ((map_of_aliveness[x][y] == True) and (2 <= alive_counter <= 3)) or ((map_of_aliveness[x][y] == False) and (alive_counter == 3)):
        return True

    return False


def count_alive_neighbours_left(x, y, map_of_aliveness):
    counter = 0
    for i in range(x, x+2):
        for j in range(y-1, y+2):
            if i == x and j == y:
                continue

            if map_of_aliveness[i][j] == True:
                counter += 1
    return counter


def count_alive_neighbours_right(x, y, map_of_aliveness):
    counter = 0
    for i in range(x-1, x+1):
        for j in range(y-1, y+2):
            if i == x and j == y:
                continue

            if map_of_aliveness[i][j] == True:
                counter += 1
    return counter


def count_alive_neighbours_top(x, y, map_of_aliveness):
    counter = 0
    for i in range(x-1, x+2):
        for j in range(y, y+2):
            if i == x and j == y:
                continue

            if map_of_aliveness[i][j] == True:
                counter += 1
    return counter


def count_alive_neighbours_bottom(x, y, map_of_aliveness):
    counter = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+1):
            if i == x and j == y:
                continue

            if map_of_aliveness[i][j] == True:
                counter += 1
    return counter


def count_alive_neighbours_inside(x, y, map_of_aliveness):
    counter = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i == x and j == y:
                continue

            if map_of_aliveness[i][j] == True:
                counter += 1
    return counter


def main():

    run = True
    start_animation = False
    clock = pygame.time.Clock()
    map_of_aliveness = [['0' for x in range(91)] for y in range(55)]

    # grid setup
    WIN.fill(BLACK)
    set_starting_grid(map_of_aliveness)
    set_starting_alive_cells(map_of_aliveness)
    draw_grid(map_of_aliveness)
    pygame.display.update()

    # handle_next_gen(dict_alive_bool)
    # animation loop
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        key_pressed = pygame.key.get_pressed()

        # animation starts
        if key_pressed[pygame.K_SPACE]:
            start_animation = True

        # animation pauses
        if key_pressed[pygame.K_p]:
            start_animation = False

        # animation resets
        if key_pressed[pygame.K_r]:
            start_animation = False
            WIN.fill(BLACK)
            set_starting_grid(map_of_aliveness)
            set_starting_alive_cells(map_of_aliveness)
            draw_grid(map_of_aliveness)
            pygame.display.update()

        # animation
        if start_animation:
            map_of_aliveness = handle_next_gen(map_of_aliveness)
            draw_grid(map_of_aliveness)
            pygame.display.update()

        # animation next gen
        if key_pressed[pygame.K_RIGHT]:
            map_of_aliveness = handle_next_gen(map_of_aliveness)
            draw_grid(map_of_aliveness)
            pygame.display.update()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
