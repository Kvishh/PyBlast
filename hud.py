import pygame
from configs import *

class HUD:
    def __init__(self, player):
        self.player = player
        self.heart = pygame.transform.scale(pygame.image.load("assets/images/heart.png").convert_alpha(), (HEART_IMAGE_WIDTH, HEART_IMAGE_HEIGHT))
        self.empty_heart = pygame.transform.scale(pygame.image.load("assets/images/empty_heart.png").convert_alpha(), (EMPTY_HEART_IMAGE_WIDTH, EMPTY_HEART_IMAGE_HEIGHT))
        self.shield = pygame.transform.scale(pygame.image.load("assets/images/shield.png").convert_alpha(), (SHIELD_IMAGE_WIDTH, SHIELD_IMAGE_HEIGHT))
    
    def update(self):
        self._blit_heart()
        self._blit_shield()

    def _blit_heart(self):
        empty_num = 0
        if self.player.current_hp < self.player.max_hp :
            empty_num = self.player.max_hp - self.player.current_hp

        for i in range(self.player.current_hp):
            display.blit(self.heart, (i*(HEART_IMAGE_WIDTH + 10), 30))
        
        if empty_num != 0:
            for i in range(self.player.current_hp, self.player.current_hp+empty_num):
                display.blit(self.empty_heart, (i*(EMPTY_HEART_IMAGE_WIDTH + 10), 30))
    
    def _blit_shield(self):
        display.blit(self.shield, (10, 70))