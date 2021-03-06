import game_functions as gf
import settings
from alien_fleet import AlienFleet
from landing_page import LandingPage
from lasers import Lasers
from scoreboard import Scoreboard
from ship import Ship
import pygame as pg
from time import sleep
from stats import Stats


class Game:
    RED = (255, 0, 0)

    def __init__(self):
        pg.init()
        self.settings = settings.Settings()
        self.stats = Stats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))

        self.bg = pg.image.load("images/bg.png")

        self.music = pg.mixer.Sound("audio/music.mp3")
        self.music.set_volume(0.3)
        self.music.play(-1)

        self.bg_color = self.settings.bg_color
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.sb = Scoreboard(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.lasers = Lasers(game=self)
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.lasers)

    def restart(self):
        if self.stats.ships_left == 0:
            self.game_over()
        print("restarting game")

        self.lasers.empty()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.update()
        self.draw()
        sleep(2)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.lasers.update()
        self.sb.update()

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.lasers.draw()
        self.sb.draw()

        pg.display.flip()

    def play(self):
        self.finished = False
        while not self.finished:
            self.update()
            self.draw()
            gf.check_events(game=self)  # exits game if QUIT pressed
        self.game_over()

    def game_over(self):
        print('\nGAME OVER!\n\n')
        exit()


def main():
    g = Game()
    lp = LandingPage(game=g)
    lp.show()
    g.play()


if __name__ == '__main__':
    main()
