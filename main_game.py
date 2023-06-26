from controls import Player
from create_sprites import *
from ray_casting import ray_casting_walls
from drawing import Draw


def main():
    pg.init()
    sc = pg.display.set_mode((wedth, height))
    pg.mouse.set_visible(False)
    sc_map = pg.Surface(radar_res)

    sprites = Sprites()
    clock = pg.time.Clock()
    player = Player(sprites)
    draw = Draw(sc, sc_map, player)

    while True:
        player.movement()

        draw.background(player.angle)

        walls = ray_casting_walls(player, draw.textures)

        draw.world(walls + [obj.object_locate(player) for obj in sprites.objects])
        draw.fps(clock)
        draw.radar(player)
        draw.player_weapon()

        pg.display.flip()
        clock.tick()


if __name__ == "__main__":
    main()
