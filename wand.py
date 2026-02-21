import pygame, math
from configs import *

class Wand(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load("assets/images/player_wand.png").convert_alpha(), -90)
        self.rect = self.image.get_rect(center=(x, y))
        self.orig_image = self.image
        self.pivot_point = self.rect.centerx/2, self.rect.centery/2
        self.offset = pygame.math.Vector2(20, 0)
    
    def update(self, player, scroll, x, y):
        mouse_pos_x = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH) + scroll[0]
        mouse_pos_y = (pygame.mouse.get_pos()[1] * DISPLAY_WIDTH / WINDOW_WIDTH) + scroll[1]
        pl_x = x
        pl_y = y
        self.rect.center = player.rect.center
        dx = mouse_pos_x - pl_x
        dy = mouse_pos_y - pl_y
        angle_mouse = math.degrees(math.atan2(dy, dx))
        self._rotate_around_pivot(angle_mouse, x, y)

    def render(self, scroll):
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def _rotate_around_pivot(self, angle, x, y):
        self.image = pygame.transform.rotate(self.orig_image, -angle)
        rotated_offset = self.offset.rotate(angle)

        self.rect = self.image.get_rect(center = (self.rect.centerx+5, self.rect.centery+6) + rotated_offset)
       