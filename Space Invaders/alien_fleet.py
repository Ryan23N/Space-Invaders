from random import randint, choice

from timer import Timer
from vector import Vector
from pygame.sprite import Group, Sprite, GroupSingle
import pygame as pg


class AlienFleet:
    alien_exploding_images = [pg.image.load(f'images/rainbow_explode{n}.png') for n in range(8)]
    alien_images = [pg.image.load(f'images/Alien-{n+1}.png') for n in range(2)]
    alien_images2 = [pg.image.load(f'images/Alien2-{n + 1}.png') for n in range(2)]
    alien_images3 = [pg.image.load(f'images/Alien3-{n + 1}.png') for n in range(2)]

    def __init__(self, game, v=Vector(1, 0)):
        self.game = game
        self.ship = self.game.ship
        self.settings = game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.v = v
        alien = Alien(self.game, image_list=AlienFleet.alien_images)
        self.alien_h, self.alien_w = alien.rect.height, alien.rect.width
        self.fleet = Group()
        self.create_fleet()

    def create_fleet(self):
        n_cols = self.get_number_cols(alien_width=self.alien_w)
        n_rows = self.get_number_rows(ship_height=self.ship.rect.height,
                                      alien_height=self.alien_h)
        for row in range(n_rows):
            for col in range(n_cols):
                self.create_alien(row=row, col=col)

    def set_ship(self, ship):
        self.ship = ship

    def create_alien(self, row, col):
        x = self.alien_w * (2 * col + 1)
        y = self.alien_h * (2 * row + 1)
        images = AlienFleet.alien_images

        if row == 3 or row == 2:
            images = AlienFleet.alien_images
            points = 10
        elif row == 1:
            images = AlienFleet.alien_images2
            points = 20
        elif row == 0:
            images = AlienFleet.alien_images3
            points = 30

        alien = Alien(game=self.game, ul=(x, y), v=self.v, image_list=images,
                      points=points)
        self.fleet.add(alien)

    def empty(self):
        self.fleet.empty()

    def get_number_cols(self, alien_width):
        spacex = self.settings.screen_width - 2 * alien_width
        return int(spacex / (2 * alien_width))

    def get_number_rows(self, ship_height, alien_height):
        spacey = self.settings.screen_height - 3 * alien_height - ship_height
        return int(spacey / (2 * alien_height))

    def length(self):
        return len(self.fleet.sprites())

    def change_v(self, v):
        for alien in self.fleet.sprites():
            alien.change_v(v)

    def check_bottom(self):
        for alien in self.fleet.sprites():
            if alien.check_bottom():
                self.ship.hit()
                break

    def check_edges(self):
        for alien in self.fleet.sprites():
            if alien.check_edges():
                return True
        return False

    def update(self):
        delta_s = Vector(0, 0)    # don't change y position in general
        if self.check_edges():
            self.v.x *= -1
            self.change_v(self.v)
            delta_s = Vector(0, self.settings.fleet_drop_speed)

        if pg.sprite.spritecollideany(self.ship, self.fleet) or self.check_bottom():
            if not self.ship.is_dying():
                self.ship.hit()

        for alien in self.fleet.sprites():
            alien.update(delta_s=delta_s)

    def draw(self):

        for alien in self.fleet.sprites():
            alien.draw()


class Alien(Sprite):
    def __init__(self, game, image_list, start_index=0, ul=(0, 100), v=Vector(1, 0), points=10):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.points = points
        self.stats = game.stats
        self.image = pg.image.load('images/alien0.bmp')
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = ul
        self.ul = Vector(ul[0], ul[1])  # position
        self.v = v  # velocity
        self.dying = False

        self.explosion_sound = pg.mixer.Sound("audio/explosion.wav")
        self.explosion_sound.set_volume(0.1)

        self.image_list = image_list
        self.exploding_timer = Timer(image_list=AlienFleet.alien_exploding_images, delay=200,
                                     start_index=start_index, is_loop=False)
        self.normal_timer = Timer(image_list=image_list, delay=1000, is_loop=True)
        self.timer = self.normal_timer

    def change_v(self, v):
        self.v = v

    def check_bottom(self):
        return self.rect.bottom >= self.screen_rect.bottom

    def check_edges(self):
        r = self.rect
        return r.right >= self.screen_rect.right or r.left <= 0

    def update(self, delta_s=Vector(0, 0)):
        if self.dying and self.timer.is_expired():
            self.kill()

        self.ul += delta_s
        self.ul += self.v * self.settings.alien_speed_factor
        self.rect.x, self.rect.y = self.ul.x, self.ul.y

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)

    def hit(self):
        self.stats.alien_hit(alien=self)
        self.explosion_sound.play()
        self.timer = self.exploding_timer
        self.dying = True


# class Ufo(Sprite):
#     def __init__(self, game, side='right', screen_width=50):
#         super().__init__()
#         self.game = game
#
#
#         # self.ufo_images = [pg.image.load(f'images/ufo{n}.png') for n in range(5)]
#         self.ufo_images = pg.image.load(f'images/ufo0.png').convert_alpha()
#
#         if side == 'right':
#             x = screen_width + 50
#             self.speed = - 3
#         else:
#             x = -50
#             self.speed = 3
#
#         self.rect = self.ufo_images.get_rect(topleft=(x, 80))
#
#         # self.ufo = GroupSingle()
#         # self.ufo_spawn_time = randint(40, 80)
#
#     def ufo_timer(self):
#         self.game.ufo_spawn_time -= 1
#         if self.game.ufo_spawn_time <= 0:
#             self.game.ufo.add(Ufo(choice(['right', 'left']), self.game.settings.screen_width))
#             self.game.ufo_spawn_time = randint(400, 800)
#
#     def draw(self):
#         rect = self.ufo_images.get_rect()
#         rect.x, rect.y = self.rect.x, self.rect.y
#         self.ufo_timer()
#         self.game.screen.blit(self.ufo_images, self.rect)
#
#     def update(self):
#         self.rect.x += self.speed
