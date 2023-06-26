import pygame as pg
from settings import *
from map import radar
from collections import deque


class Draw:
    def __init__(self, sc, sc_map, player):
        self.sc = sc
        self.sc_map = sc_map
        self.player = player
        self.font = pg.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pg.image.load('img/wall3.png').convert(),
                         2: pg.image.load('img/wall4.png').convert(),
                         3: pg.image.load('img/wall5.png').convert(),
                         4: pg.image.load('img/wall6.png').convert(),
                         'S': pg.image.load('img/sky1.png').convert()
                         }
        #gun
        self.weapon_base = pg.image.load('sprites/gun/shotgun/base/0.png').convert_alpha()
        self.shot_anim = deque([pg.image.load(f'sprites/gun/shotgun/anim/{i}.png').convert_alpha()
                                  for i in range(20)])

        self.weapon_rect = self.weapon_base.get_rect()
        self.weapon_pos = (hw - self.weapon_rect.width // 2, height - self.weapon_rect.height)
        self.shot_len = len(self.shot_anim)
        self.weapon_len_count = 0
        self.weapon_anim_speed = 3
        self.shot_anim_count = 0
        self.shot_anim_trigger = True


    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % wedth
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - wedth, 0))
        self.sc.blit(self.textures['S'], (sky_offset + wedth, 0))
        pg.draw.rect(self.sc, darkgray, (0, hh, wedth, hh))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, blue)
        self.sc.blit(render, fps_pos)

    def radar(self, player):
        self.sc_map.fill(black)
        map_x, map_y = player.x // map_scale, player.y // map_scale
        pg.draw.circle(self.sc, darkgray, (hw, hh), 4)
        pg.draw.circle(self.sc_map, red, (int(map_x), int(map_y)), 5)
        pg.draw.line(self.sc_map, yellow, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                           map_y + 12 * math.sin(player.angle)), 2)
        for x, y in radar:
            pg.draw.rect(self.sc_map, sandy, (x, y, map_tile, map_tile))
        self.sc.blit(self.sc_map, map_pos)

    def player_weapon(self):
        if self.player.shot:
            shot_sprite = self.shot_anim[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_anim_count += 1
            if self.shot_anim_count == self.weapon_anim_speed:
                self.shot_anim.rotate(-1)
                self.shot_anim_count = 0
                self.weapon_len_count += 1
                self.shot_anim_trigger = False
            if self.weapon_len_count == self.shot_len:
                self.player.shot = False
                self.weapon_len_count = 0
                self.shot_anim_trigger = True
        else:
            self.sc.blit(self.weapon_base, self.weapon_pos)