import pygame
from pygame.math import Vector2
import random
from scripts.name_path import PATH_TO_ENEMY_NORMAL
from scripts.name_path import PATH_TO_ENEMY_HUNT_MODE_ACTIVE
from scripts.code_const import SIZE_CAGE, COUNT_CAGES_WIDTH, SPEED_ENEMY

class Enemy:
    SPRITES = {}  # словарь спрайтой для каждого номера

    def __init__(self, enemy_count, screen, start_pos):
        self._speed = SPEED_ENEMY
        size_of_road = SIZE_CAGE // 2
        self._DIRECTIONS = {(-self._speed, 0): ((-self._speed, 0), (0, -self._speed), (0, self._speed)),
                            (self._speed, 0): ((self._speed, 0), (0, -self._speed), (0, self._speed)),
                            (0, -self._speed): ((0, -self._speed), (-self._speed, 0), (self._speed, 0)),
                            (0, self._speed): ((0, self._speed), (-self._speed, 0), (self._speed, 0))}
        self._CHECK = {(-self._speed, 0): (-size_of_road, 0),
                       (self._speed, 0): (size_of_road, 0),
                       (0, -self._speed): (0, -size_of_road),
                       (0, self._speed): (0, size_of_road)}

        self._sprite = pygame.image.load(PATH_TO_ENEMY_NORMAL)
        self._screen = screen
        self._collider = self._sprite.get_rect()
        center = self._collider.center
        self._collider.w //= 2
        self._collider.h //= 2
        self._collider.center = center
        self._coords = Vector2(*start_pos)
        self._hunt_mode = True
        self._direction = random.choice(((-self._speed, 0), (0, -self._speed)))
        self._start_pos = Vector2(*start_pos)

    def render(self):
        self._collider.topleft = self._coords
        self.update()

    def update(self):
        self._screen.blit(self._sprite, self._collider)
    
    def get_rect(self):
        return self._collider

    def move(self, map_object):
        map_coords = map_object.get_coords()
        map_size = map_object.size
        x = self._collider.x + self._CHECK[self._direction][0] + self._collider.w
        y = self._collider.y + self._CHECK[self._direction][1] + self._collider.h
        object = map_object.get_object_rect((x, y))
        pref_direction = self._direction
        while object == 'W':
            now_direction = random.choice(self._DIRECTIONS[self._direction])
            while pref_direction + now_direction == (0, 0):
                now_direction = random.choice(self._DIRECTIONS[self._direction])
            self._direction = now_direction    
            x = self._collider.x + self._CHECK[self._direction][0] + self._collider.w
            y = self._collider.y + self._CHECK[self._direction][1] + self._collider.h
            object = map_object.get_object_rect((x, y))
        
        self._coords += self._direction
        self._collider.topleft = self._coords
        if self._collider.bottomright[0] <= map_coords[0]:
            self._collider.topleft = (map_coords[0] + COUNT_CAGES_WIDTH * SIZE_CAGE, self._collider.y)
            self._coords = (map_coords[0] + COUNT_CAGES_WIDTH * SIZE_CAGE, self._collider.y)
        elif self._collider.bottomleft[0] >= map_coords[0] + map_size[0]:
            self._collider.topleft = (map_coords[0], self._collider.y)
            self._coords = (map_coords[0], self._collider.y)

    #  to do it
    def change_mode(self):
        self._hunt_mode = not self._hunt_mode

        if self._hunt_mode:
            self._sprite = pygame.image.load(PATH_TO_ENEMY_NORMAL)  # замена спрайта
        else:
            self._sprite =  pygame.image.load(PATH_TO_ENEMY_HUNT_MODE_ACTIVE)  # замена спрайта

    def return_to_start(self):
        self._coords = self._start_pos.copy()
        self._collider.topleft = self._coords
        self.update()
    
    # to do it
    def die(self):
        self._coords = self._start_pos.copy()
        self._hunt_mode = False
        self._direction = random.choice(((-self._speed, 0), (0, -self._speed)))