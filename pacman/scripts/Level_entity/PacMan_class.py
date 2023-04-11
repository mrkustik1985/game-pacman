import pygame
from pygame.math import Vector2
import time
from scripts.name_path import PATH_TO_PACMAN
from scripts.code_const import SIZE_CAGE, COUNT_CAGES_WIDTH, PACMAN_SPEED

class PacMan:
    def __init__(self, screen, start_pos):
        self._screen = screen
        pygame.sprite.Sprite.__init__(self)
        self._speed = PACMAN_SPEED
        self._coords = Vector2(*start_pos)
        self._start_pos = start_pos
        
        self._sprite = pygame.image.load(PATH_TO_PACMAN)
        self._sprite_print = pygame.image.load(PATH_TO_PACMAN)
        self._collider = self._sprite.get_rect()

        # decrease size of sprite
        center = self._collider.center
        self._collider.w //= 2
        self._collider.h //= 2
        self._collider.center = center

        self._lives = 3
        self._score = 0
        self._direct = None
        self._direction = [(0, 0), (0, 0)]
        self._start_pos = Vector2(*start_pos).copy()

        self.init_logoc_of_moving()

    def init_logoc_of_moving(self):
        size_of_road = SIZE_CAGE // 2 + 1 # road size / 2 to get center
        self._DELTA = {pygame.K_a: (Vector2(-self._speed, 0), (-size_of_road, 0)),
                       pygame.K_s: (Vector2(0, self._speed), (0, size_of_road)),
                       pygame.K_d: (Vector2(self._speed, 0), (size_of_road, 0)),
                       pygame.K_w: (Vector2(0, -self._speed), (0, -size_of_road)),
                       pygame.K_LEFT: (Vector2(-self._speed, 0), (-size_of_road, 0)),
                       pygame.K_DOWN: (Vector2(0, self._speed), (0, size_of_road)),
                       pygame.K_RIGHT: (Vector2(self._speed, 0), (size_of_road, 0)),
                       pygame.K_UP: (Vector2(0, -self._speed), (0, -size_of_road))}
        self._turn = {
                    pygame.K_LEFT: 180,
                    pygame.K_DOWN: 270,
                    pygame.K_RIGHT: 0,
                    pygame.K_UP: 90
                    }

    def render(self):
        self._collider.center= self._coords
        self.update()

    def update(self):
        rot_image = pygame.transform.rotate(self._sprite, self._turn.get(self._direct, 0))
        self._screen.blit(rot_image, self._collider)

    def eat_coins(self, objects):
        rects = list(map(lambda x: x.get_rect(), objects))
        indexes = self._collider.collidelistall(rects)
        for ind in indexes:
            objects[ind].got_eaten()
            self._score += objects[ind].get_price()
            break

    def eat_special_coins(self, objects):
        rects = list(map(lambda x: x.get_rect(), objects))
        indexes = self._collider.collidelistall(rects)
        for ind in indexes:
            objects[ind].got_eaten()
            self._score += objects[ind].get_price()
            break
        return len(indexes) != 0
    
    def move(self, map_object):
        try:
            map_coords = map_object.get_coords()
            map_size = map_object.size
            x = self._collider.center[0] + self._direction[1][0] + self._collider.w // 2
            y = self._collider.center[1] + self._direction[1][1] + self._collider.h // 2
            object = map_object.get_object_rect((x, y))
            if object not in "WGH":
                self._coords += self._direction[0]
                self._collider.topleft = self._coords
                if self._collider.bottomright[0] <= map_coords[0]:
                    self._collider.topleft = (map_coords[0] + COUNT_CAGES_WIDTH * SIZE_CAGE, self._collider.y)
                    self._coords = (map_coords[0] + COUNT_CAGES_WIDTH * SIZE_CAGE, self._collider.y)
                elif self._collider.bottomleft[0] >= map_coords[0] + map_size[0]:
                    self._collider.topleft = (map_coords[0], self._collider.y)
                    self._coords = (map_coords[0], self._collider.y)
        except KeyError:
            pass
    
    def change_direction(self, direction, map_object):
        try:
            x = self._collider.x + self._DELTA[direction][1][0] + self._collider.w
            y = self._collider.y + self._DELTA[direction][1][1] + self._collider.h
            object = map_object.get_object_rect((x, y))
            if object not in "WGH":
                self._direction = self._DELTA[direction]
                self._direct = direction
        except KeyError:
            pass

    def get_lives(self):
        return self._lives

    def get_score(self):
        return self._score

    def damage(self):
        self._lives -= 1

    def get_rect(self):
        return self._collider

    def return_to_start(self):
        self._coords = self._start_pos.copy()
        self._collider.topleft = self._coords
        self._direct = None
        self._direction = [(0, 0), (0, 0)]
        self._pref_direction = [(0, 0), (0, 0)]
        self._pref_direct = [(0, 0), (0, 0)]
        self.update()
    def eat_enemy(self):
        self._score += 300