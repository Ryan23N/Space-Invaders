import sys
import pygame as pg
from lasers import Laser
from vector import Vector


LEFT, RIGHT, STOP = 'left', 'right', 'stop'

dirs = {LEFT: Vector(-1, 0),
        RIGHT: Vector(1, 0),
        STOP: Vector(0, 0)}

dir_keys = {pg.K_LEFT: LEFT, pg.K_a: LEFT,
            pg.K_RIGHT: RIGHT, pg.K_d: RIGHT}


def check_events(game):
    laser_sound = pg.mixer.Sound("audio/laser.wav")
    laser_sound.set_volume(0.1)
    ship = game.ship
    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()
        elif e.type == pg.KEYDOWN:
            if e.key in dir_keys:
                v = dirs[dir_keys[e.key]]
                ship.inc_add(v)
            elif e.key == pg.K_SPACE:
                laser_sound.play()
                new_laser = Laser(game)
                game.lasers.add(new_laser)
        elif e.type == pg.KEYUP:
            if e.key in dir_keys:
                v = dirs[dir_keys[e.key]]
                ship.inc_add(-v)
