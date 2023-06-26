import pygame as pg
from settings import *
from map import world_map, world_h, world_w
import numpy as np
from numba import njit


@njit(fastmath=True, parallel=True)
def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


@njit(fastmath=True, parallel=True)
def ray_casting(player_pos, player_angle, world_map):
    casted_walls = []
    ox, oy = player_pos
    texture_h, texture_v = 1, 1
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - hf
    for ray in range(num_rays):
        sin_a = np.sin(cur_angle)
        cos_a = np.cos(cur_angle)

        # vert
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, world_w, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        # hori
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, world_h, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE
        # proj
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= np.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_h1 = int(proj_coeff / depth)

        casted_walls.append((depth, offset, proj_h1, texture))
        cur_angle += delta_angle
    return casted_walls

def ray_casting_walls(player, textures):
    casted_wall = ray_casting(player.pos, player.angle, world_map)
    walls = []
    for ray,casted_values in enumerate(casted_wall):
        depth, offset, proj_h1, texture = casted_values
        if proj_h1 > height:
            coeff = proj_h1 / height
            texture_height1 = texture_height / coeff
            wall_col = textures[texture].subsurface(offset * texture_s,
                                                    texture_height // 2 - texture_height1 // 2,
                                                    texture_s,
                                                    texture_height1)

            wall_col = pg.transform.scale(wall_col, (scale, height))
            wall_pos = (ray * scale, 0)
        else:
            wall_col = textures[texture].subsurface(offset * texture_s, 0, texture_s, texture_height)
            wall_col = pg.transform.scale(wall_col, (scale, proj_h1))
            wall_pos = (ray * scale, hh - proj_h1 // 2)

        walls.append((depth, wall_col, wall_pos))
    return walls
