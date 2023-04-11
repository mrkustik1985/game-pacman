import pygame
from scripts.UI.Button import Button
from scripts.name_path import PATH_TO_GLOBAL_MENU
from scripts.name_path import PATH_TO_UI
from scripts.code_const import LOCATION_BUTTON, SETBACK_BUTTON

class Menu:
    def __init__(self, screen):
        self._screen = screen
        self._menu = pygame.image.load(PATH_TO_GLOBAL_MENU)
        self._quit = Button(*LOCATION_BUTTON, PATH_TO_UI + '/quit1.png', PATH_TO_UI + '/quit2.png', screen)
        self._play = Button(LOCATION_BUTTON[0], self._quit.get_rect()[1] - SETBACK_BUTTON, PATH_TO_UI + '/play1.png', PATH_TO_UI + '/play2.png', screen)

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
            self._screen.blit(self._menu, (self._play.get_rect()[0], self._play.get_rect()[1] - SETBACK_BUTTON))
            self._quit.render()
            self._play.render()

            play_pressed = self._play.is_pressed()
            quit_pressed = self._quit.is_pressed()
            if play_pressed:
                break
            elif quit_pressed:
              exit(0)
            pygame.display.flip()