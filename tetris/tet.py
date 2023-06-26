import pygame as pg
from copy import deepcopy
from random import choice, randrange
from sett1 import *
from tet1 import Controls

w, h = 10, 20
t = 45
res = w * t, h * t
fps = 60
RES = 750, 940

figure_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
              [(0, -1), (-1, -1), (-1, 0), (0, 0)],
              [(-1, 0), (-1, 1), (0, 0), (0, -1)],
              [(0, 0), (-1, 0), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, 0)]]

count, speed, limit = 0, 60, 2000

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
pg.init()
sc = pg.display.set_mode(RES)
game_sc = pg.Surface(res)
clock = pg.time.Clock()

grid = [pg.Rect(x * t, y * t, t, t) for x in range(w) for y in range(h)]

figures = [[pg.Rect(x + w // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figure_pos]
figure_rect = pg.Rect(0, 0, t - 2, t - 2)
field = [[0 for i in range(w)] for j in range(h)]

figure, next_fig = deepcopy(choice(figures)), deepcopy(choice(figures))

get_color = lambda: (randrange(30, 256),
                     randrange(30, 256),
                     randrange(30, 256)
                     )
color, next_c = get_color(), get_color()

bg = pg.image.load('img/text1.jpg').convert()
game_bg = pg.image.load('img/text1.jpg').convert()

main_font = pg.font.Font('font/font.ttf', 65)
font = pg.font.Font('font/font.ttf', 45)
title_tt = main_font.render("TETRIS", True, pg.Color("darkorange"))
title_score = font.render('score:', True, pg.Color('green'))
title_record = font.render("record:", True, pg.Color('purple'))

player = Controls(dx, rotate, pause)


def check():
    if figure[i].x < 0 or figure[i].x > w - 1:
        return False
    elif figure[i].y > h - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    player = Controls(dx, rotate, pause)
    record = get_record()
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # delay
    for i in range(lines):
        pg.time.wait(200)
    # controls
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            exit()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    dx = -1
                elif event.key == pg.K_RIGHT:
                    dx = 1
                elif event.key == pg.K_DOWN:
                    limit = 100
                elif event.key == pg.K_ESCAPE:
                    exit()
                elif event.key == pg.K_UP:
                    rotate = True
                if event.type == pg.KEYUP:
                    rotate = True
                if event.key == pg.K_p:
                    pause = True
    while player.pause:
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    pause = False
    # player.movement()
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += player.dx
        if not check():
            figure = deepcopy(figure_old)
            break
    # move y
    count += speed
    if count > limit:
        count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_fig, next_c
                next_fig, next_c = deepcopy(choice(figures)), get_color()
                limit = 2000
                break
    # rotate
    figure_old = deepcopy(figure)
    center = figure[0]
    if player.rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check():
                figure = deepcopy(figure_old)
                break
    # -last line
    line, lines = h - 1, 0
    for row in range(h - 1, -1, -1):
        c = 0
        for i in range(w):
            if field[row][i]:
                c += 1
            field[line][i] = field[row][i]
        if c < w:
            line -= 1
        else:
            speed += 3
            lines += 1
    # score
    score += scores[lines]
    # grid
    [pg.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # figure
    for i in range(4):
        figure_rect.x = figure[i].x * t
        figure_rect.y = figure[i].y * t
        pg.draw.rect(game_sc, color, figure_rect)
    # field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x = x * t
                figure_rect.y = y * t
                pg.draw.rect(game_sc, col, figure_rect)
    # next_fig
    for i in range(4):
        figure_rect.x = next_fig[i].x * t + 380
        figure_rect.y = next_fig[i].y * t + 185
        pg.draw.rect(sc, next_c, figure_rect)
    # titles
    sc.blit(title_tt, (485, -10))
    sc.blit(title_score, (535, 780))
    sc.blit(font.render(str(score), True, pg.Color("blue")), (550, 840))
    sc.blit(title_record, (525, 650))
    sc.blit(font.render(record, True, pg.Color('gold')), (550, 710))
    # over
    for i in range(w):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(w)] for j in range(h)]
            count, speed, limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pg.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pg.display.flip()
                clock.tick(200)
    pg.display.flip()
    clock.tick(fps)
