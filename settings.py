import math

# game settings
wedth = 1200
height = 800
hw = wedth // 2
hh = height // 2
penta_h = 5 * height
double_h = 2 * height
FPS = 400
TILE = 100
fps_pos = (wedth - 65, 5)

# radar
radar_scale = 5
radar_res = wedth // radar_scale, height // radar_scale
map_scale = 2 * radar_scale
map_tile = TILE // map_scale
map_pos = (0, 0)

# ray settings
fov = math.pi / 3
hf = fov / 2
num_rays = 300
max_depth = 800
delta_angle = fov / num_rays
dist = num_rays / (2 * math.tan(hf))
proj_coeff = 3 * dist * TILE
scale = wedth // num_rays

# sprites
d_pi = 2 * math.pi
middle_ray = num_rays // 2 - 1
fake_rays = 100
fake_rays_range = num_rays - 1 + 2 * fake_rays

# textures(1200 x 1200)
texture_wight = 1200
texture_height = 1200
half_text_h = texture_height // 2
texture_s = texture_wight // TILE

# player settings
player_pos = hw // 4, hh - 50
player_angle = 0
player_speed = 2

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (220, 0, 0)
green = (0, 80, 0)
blue = (0, 0, 255)
darkgray = (40, 40, 40)
purple = (120, 0, 120)
skyblue = (0, 186, 255)
yellow = (220, 220, 0)
sandy = 244, 164, 96
