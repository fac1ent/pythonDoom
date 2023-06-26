from settings import *
import pygame as pg
import numpy as np
from map import coll


class Player:
    def __init__(self, sprites):
        self.x, self.y = player_pos
        self.sprites = sprites
        self.angle = player_angle
        self.player_speed = player_speed
        self.sens = 0.003
        self.side = 50
        self.rect = pg.Rect(*player_pos, self.side, self.side)

        #gun
        self.shot =  False

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def coll_list(self):
        return coll + [pg.Rect(*obj.pos, obj.side, obj.side)for obj in
                     self.sprites.objects if obj.blocked]

    def detect(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)

        hits = next_rect.collidelistall(self.coll_list)

        if len(hits):
            delta_x, delta_y = 0, 0
            for hit in hits:
                hit_rect = self.coll_list[hit]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left

                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys()
        self.mouse()
        self.rect.center = self.x, self.y
        self.angle %= d_pi

    def keys(self):
        sin_a = np.sin(self.angle)
        cos_a = np.cos(self.angle)

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            exit()

        if keys[pg.K_w]:
            if keys[pg.K_LSHIFT]:
                dx = (2 + player_speed) * cos_a
                dy = (2 + player_speed) * sin_a
                self.detect(dx, dy)
            else:
                dx = player_speed * cos_a
                dy = player_speed * sin_a
                self.detect(dx, dy)

        if keys[pg.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect(dx, dy)

        if keys[pg.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect(dx, dy)

        if keys[pg.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect(dx, dy)


        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True


    def mouse(self):
        mouse = pg.mouse
        if mouse.get_focused():
            diff = mouse.get_pos()[0] - hw
            mouse.set_pos((hw, hh))
            self.angle += diff * self.sens
