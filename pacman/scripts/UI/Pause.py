import pygame
import time
from scripts.UI.Button import Button
from scripts.name_path import PATH_TO_UI
from scripts.code_const import LOCATION_BUTTON, SETBACK_BUTTON

class Pause:
    def __init__(self, screen):
        self._screen = screen
        self._pause = pygame.image.load(PATH_TO_UI + '/pause.png')
        self._menu = Button(*LOCATION_BUTTON, PATH_TO_UI + '/quit1.png', PATH_TO_UI + '/quit2.png', screen)
        self._resume = Button(self._menu.get_rect()[0], self._menu.get_rect()[1] - SETBACK_BUTTON, 
                       PATH_TO_UI + '/resume1.png', PATH_TO_UI + '/resume2.png', screen)
        self.stop = False
    def render(self):
        while True:
            self._screen.fill("BLACK")
            for e in pygame.event.get():
              if e.type == pygame.QUIT:
                exit(0)
              if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                  exit(0)
                if e.key == pygame.K_SPACE:
                   return 1
            self._screen.blit(self._pause, (self._resume.get_rect()[0], self._resume.get_rect()[1] - SETBACK_BUTTON))
            self._resume.render()
            self._menu.render()

            resume_pressed = self._resume.is_pressed()
            menu_pressed = self._menu.is_pressed()
            if resume_pressed:
                break
            elif menu_pressed:
              self.stop = True
              exit(0)
            pygame.display.flip()
