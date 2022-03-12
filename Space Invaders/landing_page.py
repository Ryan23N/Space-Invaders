import pygame as pg
import sys
from alien_fleet import Alien
from vector import Vector
from button import Button

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)


class LandingPage:
    alien_one_imgs = [pg.image.load(f'images/Alien-{n+1}.png') for n in range(2)]
    alien_two_imgs = [pg.image.load(f'images/Alien2-{n+1}.png') for n in range(2)]
    alien_three_imgs = [pg.image.load(f'images/Alien3-{n+1}.png') for n in range(2)]
    ufo_imgs = [pg.image.load(f'images/ufo{n}.png') for n in range(5)]

    def __init__(self, game):
        self.screen = game.screen
        self.landing_page_finished = False
        self.highscore = game.stats.get_highscore()

        self.bg = pg.image.load("images/bg.png")

        headingFont = pg.font.SysFont(None, 192)
        subheadingFont = pg.font.SysFont(None, 122)
        font = pg.font.SysFont(None, 48)

        strings = [('SPACE', WHITE, headingFont), ('INVADERS', GREEN, subheadingFont),
                   ('= 10 PTS', GREY, font), ('= 20 PTS', GREY, font),
                   ('= 40 PTS', GREY, font), ('= ???', GREY, font),
                   (f'HIGH SCORE = {self.highscore:,}', GREY, font)]

        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]

        self.posns = [150, 230]
        alien = [60 * x + 400 for x in range(4)]
        self.posns.extend(alien)
        self.posns.append(730)

        centerx = self.screen.get_rect().centerx

        self.play_button = Button(self.screen, "PLAY GAME", ul=(centerx - 150, 650))

        n = len(self.texts)
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]

        self.alien_one = Alien(game=game, image_list=LandingPage.alien_one_imgs,
                               v=Vector(), ul=(centerx - 150, 362))

        self.alien_two = Alien(game=game, image_list=LandingPage.alien_two_imgs,
                               v=Vector(), ul=(centerx - 150, 420))

        self.alien_three = Alien(game=game, image_list=LandingPage.alien_three_imgs,
                                 v=Vector(), ul=(centerx - 150, 490))

        self.ufo = Alien(game=game, image_list=LandingPage.ufo_imgs,
                         v=Vector(), ul=(centerx - 145, 550))

        self.hover = False

    def get_text(self, font, msg, color):
        return font.render(msg, True, color, BLACK)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def mouse_button(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.play_button.rect.collidepoint(mouse_x, mouse_y)

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYUP and e.key == pg.K_p:  # pretend PLAY BUTTON pressed
                self.landing_page_finished = True
            elif e.type == pg.MOUSEBUTTONDOWN:
                if self.mouse_button():
                    self.landing_page_finished = True
            elif e.type == pg.MOUSEMOTION:
                if self.mouse_button() and not self.hover:
                    self.play_button.toggle_color()
                    self.hover = True
                elif not self.mouse_button() and self.hover:
                    self.play_button.toggle_color()
                    self.hover = False

    def show(self):
        while not self.landing_page_finished:
            self.draw()
            self.check_events()  # exits game if QUIT pressed

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.bg, (0, 0))
        self.alien_one.draw()
        self.alien_two.draw()
        self.alien_three.draw()
        self.ufo.draw()
        self.draw_text()
        self.play_button.draw()
        pg.display.flip()
