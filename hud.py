import pygame
from configs import *

class HUD:
    def __init__(self, player):
        self.font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 30)
        self.player = player
        self.heart = pygame.transform.scale(pygame.image.load("assets/images/heart.png").convert_alpha(), (HEART_IMAGE_WIDTH, HEART_IMAGE_HEIGHT))
        self.empty_heart = pygame.transform.scale(pygame.image.load("assets/images/empty_heart.png").convert_alpha(), (EMPTY_HEART_IMAGE_WIDTH, EMPTY_HEART_IMAGE_HEIGHT))
        self.shield = pygame.transform.scale(pygame.image.load("assets/images/shield.png").convert_alpha(), (SHIELD_IMAGE_WIDTH, SHIELD_IMAGE_HEIGHT))
    
    def update(self):
        self._blit_heart()
        self._blit_shield()
        self.blit_FPS()


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
    
    def blit_FPS(self):
        text = self.render_outlined((f"FPS: {clock.get_fps():.0f}"), (255,255,255), (0,0,0), 2)
        display.blit(text, (DISPLAY_WIDTH-100,0))
    
    def render_outlined(self, text: str, text_color: pygame.typing.ColorLike, outline_color: pygame.typing.ColorLike, outline_width: int,) -> pygame.Surface:
        old_outline = self.font.outline
        if old_outline != 0:
            self.font.outline = 0
        base_text_surf = self.font.render(text, False, text_color)
        self.font.outline = outline_width
        outlined_text_surf = self.font.render(text, True, outline_color)

        outlined_text_surf.blit(base_text_surf, (outline_width, outline_width))
        self.font.outline = old_outline
        return outlined_text_surf