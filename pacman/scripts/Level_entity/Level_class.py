import pygame
import time

from scripts.Level_entity.Coins_class import Coin, SpecialCoin
from scripts.Level_entity.Map_class import Map, WIDTH, HEIGHT
from scripts.Level_entity.Enemies_class import Enemy
from scripts.Level_entity.PacMan_class import PacMan
from scripts.UI.Button import Button
from scripts.UI.Pause import Pause
from scripts.name_path import PATH_TO_HEART, PATH_TO_WIN, PATH_TO_GAME_OVER
from scripts.name_path import PATH_TO_MENU_NOT_TOUCHED, PATH_TO_MENU
from scripts.code_const import WIDTH, HEIGHT, TIME_TO_WAIT
from scripts.code_const import SIZE_CAGE, COUNT_CAGES_WIDTH, COUNT_CAGES_HEIGHT
from scripts.code_const import LOCATION_BUTTON, SETBACK_BUTTON

class Level:
    #number level
    def __init__(self, number, screen):
        self.number = number
        self._screen = screen
        self._coins = []
        self._special_coins = []
        self._map = Map()
        self._player = None # late init because need coordinates
        self._score_label = pygame.font.Font(None, 30).render("0", True, pygame.Color("white"))
        self._enemies = []
        self._sprite_heart = pygame.image.load(PATH_TO_HEART)
        self._menu = Button(LOCATION_BUTTON[0], HEIGHT - SETBACK_BUTTON, PATH_TO_MENU_NOT_TOUCHED, PATH_TO_MENU, self._screen)

    def render(self):
        self._screen.fill(pygame.Color("black"))
        x, y = self._map.get_coords()
        elem_x, elem_y = self._map.size[0] / COUNT_CAGES_WIDTH, self._map.size[1] / COUNT_CAGES_HEIGHT
        enemy_count = 0
        text_map = self._map.get_text_map()
        self._map.render(self._screen)
        x, y = self._map.get_coords()
        elem_x, elem_y = self._map.size[0] / COUNT_CAGES_WIDTH, self._map.size[1] / COUNT_CAGES_HEIGHT
        enemy_count = 0
        text_map = self._map.get_text_map()
        for i in range(len(text_map)):
            row = text_map[i]
            for j in range(len(row)):
                if row[j] == 'B':
                    self._player = PacMan(self._screen, (x + j * (elem_x + 1), y + i * elem_y))
                    self._player.render()
                elif row[j] == 'C':
                    self._coins.append(Coin((j * elem_x + x, i * elem_y + y), self._screen))
                    self._coins[-1].render()
                elif row[j] == 'S':
                    self._special_coins.append(SpecialCoin((j * elem_x + x, i * elem_y + y), self._screen))
                    self._special_coins[-1].render()
                elif row[j] == 'V':
                    self._enemies.append(Enemy(enemy_count, self._screen, (x + j * elem_x, y + i * elem_y)))
                    self._enemies[enemy_count].render()
                    enemy_count += 1
        self.heart_render()

    def heart_render(self):
        x = self._map.get_coords()[0] + self._map.size[0] * 0.9
        y = self._map.get_coords()[1] - self._sprite_heart.get_rect().height
        for i in range(self._player.get_lives()):
            self._screen.blit(self._sprite_heart, (x, y))
            x -= self._sprite_heart.get_rect().width
    
    def check_coins(self):
        new_coins = []
        for coin in self._coins:
            if not coin.get_if_eaten():
                new_coins.append(coin)

        del self._coins
        self._coins = new_coins.copy()

        new_special_coins = []
        for coin in self._special_coins:
            if not coin.get_if_eaten():
                new_special_coins.append(coin)
        del self._special_coins
        self._special_coins = new_special_coins.copy()
        if len(self._special_coins) == 0 and len(self._coins) == 0:
            return self.finish_level(True)
        return True

    def finish_level(self, is_win):
        if is_win == True:
            print_screen(self._screen, PATH_TO_WIN)
            return False
        elif self._player.get_lives() > 1:
            # continue level
            self._player.damage()
            self._player.return_to_start()
            for enemy in self._enemies:
                enemy.return_to_start()
            return True
        else:
            print_screen(self._screen, PATH_TO_GAME_OVER)
            return False
    
    def process(self):
        run = True
        start = 0
        fl = False
        while run:
            # delete last iamges
            self._player.eat_coins(self._coins)
            f1 = self._player.eat_special_coins(self._special_coins)
            run = self.check_coins()
            if run == False:
                break
            if f1:
                start = time.time()
                if fl == False:
                    for enemy in self._enemies:
                        enemy.change_mode()
                    
                fl = True
            if time.time() - start > TIME_TO_WAIT and fl == True:
                for enemy in self._enemies:
                    enemy.change_mode()
                fl = False
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = Pause(self._screen)
                        pause.render()
                        if pause.stop == True:
                            run = False
                    self._player.change_direction(event.key, self._map)
            self._player.move(self._map)

            self._screen.fill(pygame.Color("black"))
            self._map.render(self._screen)
            self.heart_render()
            
            for i in range(len(self._coins)):
                self._coins[i].render()
            for i in range(len(self._special_coins)):
                self._special_coins[i].render()
            
            self._player.render()

            for enemy in self._enemies:
                if enemy.get_rect().colliderect(self._player.get_rect()):
                    if enemy._hunt_mode:
                        run = self.finish_level(False)
                        if run == False:
                            return False
                    else:
                        enemy.die()
                        self._player.eat_enemy()
                enemy.move(self._map)
                enemy.render()
            
            #print menu to pause
            self._menu.render()
            is_pressed = self._menu.is_pressed()
            if is_pressed == True:
                pause = Pause(self._screen)
                pause.render()
                if pause.stop == True:
                    run = False
            
            # across the labirint by side
            pygame.draw.rect(self._screen, pygame.Color("black"),
                            pygame.Rect((self._map.get_coords()[0] - 50, self._map.get_coords()[1]),
                                        (50, self._map.size[1])))
            pygame.draw.rect(self._screen, pygame.Color("black"),
                            pygame.Rect((self._map.get_coords()[0] + self._map.size[0], self._map.get_coords()[1]),
                                        (50, self._map.size[1])))
            
            # add counter on screen
            x, y = self._map.get_coords()[0] + 20, self._map.get_coords()[1] - 50
            self._score_label = pygame.font.Font(None, 30).\
                render(str(self._player.get_score()), True, pygame.Color("white"))
            self._screen.blit(self._score_label, (x, y))

            pygame.display.flip()


# uses when pacman win level
def print_screen(screen, PATH_TO_IMAGE):
    rect = pygame.image.load(PATH_TO_IMAGE).get_rect()
    rect.center = (HEIGHT // 2, WIDTH // 2)
    screen.fill(pygame.Color("black"))
    screen.blit(pygame.image.load(PATH_TO_IMAGE), rect)
    pygame.display.flip()
    time.sleep(TIME_TO_WAIT)
    screen.fill(pygame.Color("black"))
    pygame.display.flip()