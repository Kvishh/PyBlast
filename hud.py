import pygame
from configs import *

class HUD:
    def __init__(self, player):
        self.font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 28)
        self.font_fps = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 26)
        self.font_timer = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 60)
        self.player = player
        self.heart = pygame.transform.scale(pygame.image.load("assets/images/heart.png").convert_alpha(), (HEART_IMAGE_WIDTH, HEART_IMAGE_HEIGHT))
        self.empty_heart = pygame.transform.scale(pygame.image.load("assets/images/empty_heart.png").convert_alpha(), (EMPTY_HEART_IMAGE_WIDTH, EMPTY_HEART_IMAGE_HEIGHT))
        self.shield = pygame.transform.scale(pygame.image.load("assets/images/shield.png").convert_alpha(), (SHIELD_IMAGE_WIDTH, SHIELD_IMAGE_HEIGHT))

        self.level_bar = pygame.Rect(10, 10, 980, 20)
    
    def update(self, timer):
        self._blit_heart()
        self._blit_shield()
        self.blit_FPS()
        self.blit_timer(timer)
        self._blit_level_bar()

    def _blit_level_bar(self):
        pygame.draw.rect(display, (0,255,0), self.level_bar)
        pygame.draw.rect(display, (255,255,255), self.level_bar, 2)

    def _blit_heart(self):
        empty_num = 0
        if self.player.current_hp < self.player.max_hp :
            empty_num = self.player.max_hp - self.player.current_hp

        for i in range(self.player.current_hp):
            display.blit(self.heart, (10+i*(EMPTY_HEART_IMAGE_WIDTH + 5), 40))
        
        if empty_num != 0:
            for i in range(self.player.current_hp, self.player.current_hp+empty_num):
                display.blit(self.empty_heart, (10+(i*(EMPTY_HEART_IMAGE_WIDTH + 5)), 40))
    
    def _blit_shield(self):
        display.blit(self.shield, (10, 85))
    
    def blit_FPS(self):
        text = self.render_outlined((f"FPS: {clock.get_fps():.0f}"), (255,255,255), (0,0,0), 2, self.font_fps)
        display.blit(text, (DISPLAY_WIDTH-75,100))

    def blit_timer(self, timer):
        timer_text = self.render_outlined(timer, (255,255,255), (0,0,0), 2, self.font_timer)
        text = self.render_outlined("Survive!", (235, 0, 0), (0,0,0), 2, self.font)
        display.blit(timer_text, (DISPLAY_WIDTH-110,25))
        display.blit(text, (DISPLAY_WIDTH-85,70))
    
    def render_outlined(self, text: str, text_color: pygame.typing.ColorLike, outline_color: pygame.typing.ColorLike, outline_width: int, font) -> pygame.Surface:
        old_outline = font.outline
        if old_outline != 0:
            font.outline = 0
        base_text_surf = font.render(text, False, text_color)
        font.outline = outline_width
        outlined_text_surf = font.render(text, True, outline_color)

        outlined_text_surf.blit(base_text_surf, (outline_width, outline_width))
        font.outline = old_outline
        return outlined_text_surf