import pygame
import time

from scripts.Level_entity.Level_class import Level
from scripts.UI.Menu import Menu
from scripts.code_const import WIDTH, HEIGHT, TIME_TO_WAIT

class Game:
    def __init__(self):
        pygame.init()
        self.level_num = 1
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.level = None
        self._menu = Menu(self.screen)


    def run(self):
        id = 0
        while True:
            self.level = Level(self.level_num, self.screen)
            self._menu.render()
            self.level.render()
            pygame.display.flip()
            time.sleep(TIME_TO_WAIT)
            self.level.process()
            self.level_num += 1