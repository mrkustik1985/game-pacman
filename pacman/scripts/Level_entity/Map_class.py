import pygame
import time
from scripts.name_path import PATH_TO_MAP_TXT, PATH_TO_MAP_PNG
from scripts.code_const import WIDTH, HEIGHT
from scripts.code_const import SIZE_CAGE, COUNT_CAGES_WIDTH, COUNT_CAGES_HEIGHT

class Map:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        with open(PATH_TO_MAP_TXT, 'r') as fin:
            self._pattern = list(map(lambda x: x.split(), fin.readlines()))

        image = pygame.image.load(PATH_TO_MAP_PNG)
        mult_y = HEIGHT * 0.7 / image.get_size()[1]
        x = int(COUNT_CAGES_WIDTH * round((image.get_size()[0] * mult_y) / COUNT_CAGES_WIDTH))
        y = int(COUNT_CAGES_HEIGHT * round((image.get_size()[1] * mult_y) / COUNT_CAGES_HEIGHT))
        self._sprite = pygame.transform.scale(image, (x, y)).convert()
        self._coords = (WIDTH // 2 - self._sprite.get_size()[0] // 2,
                        HEIGHT // 2 - self._sprite.get_size()[1] // 2) # left corner map
        self.size = (x, y) # size of map

    def render(self, screen):
        screen.blit(self._sprite, self._coords) # print on screen

    def get_object_rect(self, coords):
        # return items on that coordinates
        return self._pattern[abs(coords[1] - self._coords[1]) // SIZE_CAGE][abs(coords[0] - self._coords[0]) // SIZE_CAGE]
    
    def get_text_map(self):
        return self._pattern

    def get_coords(self): # return left corner
        return self._coords
