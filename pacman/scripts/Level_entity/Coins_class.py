import pygame
import time
from scripts.name_path import PATH_TO_COIN
from scripts.name_path import PATH_TO_SPECIAL_COIN


class Coin:
    def __init__(self, coords, screen):
        self._is_eaten = False
        self._sprite = pygame.image.load(PATH_TO_COIN)
        self._price = 50
        self._screen = screen
        self._collider = self._sprite.get_rect() # get rect from sprite

        center = self._collider.center
        self._collider.w //= 1.5
        self._collider.h //= 1.5
        self._collider.center = center
        self._coords = coords

    def render(self):
        if self._is_eaten == False:
            self._collider.topleft = self._coords
            self.update()
    def update(self):
        self._screen.blit(self._sprite, self._collider)

    def get_price(self):
        return self._price
    
    def get_rect(self):
        return self._collider
    def got_eaten(self):
        self._is_eaten = True
    def get_if_eaten(self):
        return self._is_eaten

class SpecialCoin(Coin): # monets to change hunter mode pacman and ghosts
    def __init__(self, coords, screen):
        super().__init__(coords, screen)
        self._price = 200
        self._sprite = pygame.image.load(PATH_TO_SPECIAL_COIN)
        self._collider = self._sprite.get_rect() # get rect from sprite