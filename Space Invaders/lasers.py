from random import randint

from pygame.sprite import Sprite, Group
from vector import Vector
import pygame as pg
from copy import copy


class Laser(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.w, self.h = self.settings.laser_width, self.settings.laser_height
        self.ship = game.ship

        self.rect = pg.Rect(0, 0, self.w, self.h)
        self.center = copy(self.ship.center)

        tu = 50, 255
        self.color = randint(*tu), randint(*tu), randint(*tu)

        self.v = Vector(0, -1) * self.settings.laser_speed_factor

    def update(self):
        self.center += self.v
        self.rect.x, self.rect.y = self.center.x, self.center.y

    def draw(self):
        pg.draw.rect(self.screen, color=self.color, rect=self.rect)


class Lasers:
    def __init__(self, game):
        self.game = game
        self.alien_fleet = game.alien_fleet
        self.lasers = Group()
        self.stats = game.stats

    def add(self, laser):
        self.lasers.add(laser)

    def empty(self):
        self.lasers.empty()

    def update(self):
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

        collisions = pg.sprite.groupcollide(self.alien_fleet.fleet,
                                            self.lasers,
                                            False, True)
        for alien in collisions:
            if not alien.dying:
                alien.hit()

        if self.alien_fleet.length() == 0:
            self.stats.level_up()
            self.game.restart()

        for laser in self.lasers:
            laser.update()

    def draw(self):
        for laser in self.lasers:
            laser.draw()

    def fire(self):
        new_laser = Laser(self.game)
        self.lasers.add(new_laser)
