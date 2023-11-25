import pygame
import random
import math
from pygame import mixer

pygame.init()


STOP_MUSIC = pygame.USEREVENT + 1


class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont("comicsans", 20)
    LARGE_FONT = pygame.font.SysFont("comicsans", 30)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Alorythm Visualisor")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending, timer, lst, counter, swaps, sorting, red_rect, n):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width - title.get_width() - 10, 5))

    controls1 = draw_info.FONT.render(
        "SPACE - Start sorting | R - Reset", 1, draw_info.BLACK)
    draw_info.window.blit(controls1, (draw_info.width -
                          controls1.get_width() - 10, 40))

    controls2 = draw_info.FONT.render(
        "A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls2, (draw_info.width -
                          controls2.get_width() - 10, 65))

    elements = draw_info.FONT.render(f"elements: {n}", 1, draw_info.BLACK)
    draw_info.window.blit(elements, (10, 5))

    swapped = draw_info.FONT.render(f"swaps: {swaps}", 1, draw_info.BLACK)
    draw_info.window.blit(swapped, (10, 25))

    comparisons = draw_info.FONT.render(
        f"comparisons: {counter}", 1, draw_info.BLACK)
    draw_info.window.blit(comparisons, (10, 45))

    timer = draw_info.FONT.render(
        f"time: {timer//60}.{(timer*1000//60)%1000}s", 1, draw_info.BLACK)
    draw_info.window.blit(timer, (10, 65))

    for i, val in enumerate(lst):
        x = draw_info.start_x + (i) * draw_info.block_width
        if val == draw_info.min_val:
            y = draw_info.height - \
                (val - draw_info.min_val+0.5) * draw_info.block_height
        else:
            y = draw_info.height - \
                (val - draw_info.min_val) * draw_info.block_height
        z = draw_info.block_width//2

        if sorting and red_rect == val:
            color = draw_info.RED
        else:
            color = draw_info.GRADIENTS[i % 3]
        pygame.draw.rect(draw_info.window, color,
                         (x, y, draw_info.block_width, draw_info.height))

        little_font = pygame.font.SysFont("comicsans", z)
        rect_val = little_font.render(f"{val}", 1, draw_info.BLACK)
        draw_info.window.blit(rect_val,
                              (x+draw_info.block_width//2-rect_val.get_width()//2,
                               (y + draw_info.height)//2-rect_val.get_height()//2))

    pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        if max_val-min_val + 1 >= n:
            while val in lst:
                val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def main():
    mixer.music.load('dramatic.wav')
    run = True
    timestamp = 10
    clock = pygame.time.Clock()

    timer = 0
    comparisons = 0
    swaps = 0

    try:
        n = int(input("Ile elementów chcesz posortować?\n"))
    except:
        n = 50
    min_val = 1
    max_val = n

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1100, 800, lst)

    sorting = False
    already_sorted = False
    ascending = True
    song_is_over = False

    algo_name = "Bubble Sort"

    temp = 1

    num1 = lst[temp-1]
    num2 = lst[temp]

    m = n

    red_rect = lst[0]

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == STOP_MUSIC:
                print("nara")
                mixer.music.stop()

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                already_sorted = False

                timer = 0
                comparisons = 0
                swaps = 0
                m = n


            elif event.key == pygame.K_SPACE and sorting == False and already_sorted == False:
                temp = 1
                num1 = lst[temp-1]
                num2 = lst[temp]
                sorting = True
                mixer.music.rewind()
                mixer.music.play()

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            if already_sorted:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    sorting = False
                    already_sorted = False
                    timer = 0
                    comparisons = 0
                    swaps = 0
                    m = n

        if song_is_over:
            pygame.event.post(pygame.event.Event(STOP_MUSIC))
            song_is_over = False

        if sorting:
            timer += 1
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[temp-1], lst[temp] = lst[temp], lst[temp-1]
                swaps += 1

            red_rect = lst[temp]

            if m == 1:
                sorting = False
                already_sorted = True
                song_is_over = True
                continue

            comparisons += 1

            if temp + 1 >= m:
                m -= 1
                temp = 1
                num1 = lst[temp-1]
                num2 = lst[temp]
                continue

            temp += 1
            num1 = lst[temp-1]
            num2 = lst[temp]


        draw(draw_info, algo_name, ascending, timer, lst,
             comparisons, swaps, sorting, red_rect, n)

    pygame.quit()


if __name__ == '__main__':
    main()
