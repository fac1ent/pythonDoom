import pygame as pg
from sett1 import *


class Controls:
    def __init__(self, dx, rotate, pause):
        self.rotate = rotate
        self.dx = dx
        self.limit = limit
        self.pause = pause

    def movement(self):
        self.pause = False
        for event in pg.event.get():
            if event.type == pg.quit():
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.dx = -1
                elif event.key == pg.K_RIGHT:
                    self.dx = 1
                elif event.key == pg.K_DOWN:
                    self.limit = 100
                elif event.key == pg.K_UP:
                    self.rotate = True
                if event.type == pg.KEYUP:
                    self.rotate = True
                if event.key == pg.K_p:
                    self.pause = True
