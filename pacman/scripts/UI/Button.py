import pygame
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, first_img, second_img, screen):
      pygame.sprite.Sprite.__init__(self)
      self._image = pygame.image.load(first_img)
      self._new_image = pygame.image.load(second_img)
      self._rect = self._image.get_rect()
      self._rect.x = x
      self._rect.y = y
      self._screen = screen
  
    def is_pressed(self):
      is_clicked = pygame.mouse.get_pressed()
      pos_mouse = pygame.mouse.get_pos()
      
      #is across mouse with iamge
      if self._rect.collidepoint(pos_mouse):
        self._screen.blit(self._new_image, self._rect)
        if is_clicked[0] == 1: 
          return True
      return False
    
    def get_rect(self):
      return self._rect
    
    def render(self):
      self._screen.blit(self._image, self._rect)