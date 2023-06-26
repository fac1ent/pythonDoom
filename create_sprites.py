import pygame as pg
from settings import *
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'sprite_barrel': {
                'sprite': pg.image.load('sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': 0.4,
                'animation': deque(
                    [pg.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'sprite_pin': {
                'sprite': pg.image.load('sprites/pin/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': 0.6,
                'animation': deque([pg.image.load(f'sprites/pin/anim/{i}.png').convert_alpha() for i in range(8)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'sprite_devil': {
                'sprite': [pg.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pg.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10,
                'blocked': True,
            },
            'sprite_flame': {
                'sprite': pg.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque(
                    [pg.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'animation_dist': 800,
                'animation_speed': 5,
                'blocked': False,
            },
        }

        self.objects = [
            SpriteObject(self.sprite_parameters['sprite_barrel'], (7.1, 2.1)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters['sprite_pin'], (8.7, 2.5)),
            SpriteObject(self.sprite_parameters['sprite_devil'], (7, 4)),
            SpriteObject(self.sprite_parameters['sprite_flame'], (8.6, 5.6))
        ]


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.animation_count = 0
        self.side = 30
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos1 for angle, pos1 in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        dist_sprite = math.sqrt(dx ** 2 + dy ** 2)

        alpha = math.atan2(dy, dx)
        betta = alpha - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            betta += d_pi

        delta_rays = int(betta / delta_angle)
        current_ray = middle_ray + delta_rays
        dist_sprite *= math.cos(hf - current_ray * delta_angle)

        fake_ray = current_ray + fake_rays

        if 0 <= fake_ray <= fake_rays_range and dist_sprite > 30:
            proj_hight = min(int(proj_coeff / dist_sprite * self.scale), double_h)
            proj_h_h = proj_hight // 2
            shift = proj_h_h * self.shift
            # spite to angle
            if self.viewing_angles:
                if alpha < 0:
                    alpha += d_pi
                alpha = 360 - int(math.degrees(alpha))

                for angles in self.sprite_angles:
                    if alpha in angles:
                        self.object = self.sprite_positions[angles]
                        break

            #anim
            sprite_obj = self.object
            if self.animation and dist_sprite < self.animation_dist:
                sprite_obj = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            sprite_pos = (current_ray * scale - proj_h_h, hh - proj_h_h + shift)
            sprite = pg.transform.scale(sprite_obj, (proj_hight, proj_hight))
            return dist_sprite, sprite, sprite_pos
        else:
            return False,
