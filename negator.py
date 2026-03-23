import pygame
from images import NegatorImage
from configs import *

class Negator(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.image = NegatorImage.negator_image_scaled
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2(pos)
        self.offset = pygame.Vector2(60, 0)
        self.angle = 0
    
    def update(self, player_pos, dt):
        self.pos = pygame.Vector2(player_pos)

        self.angle -= 100 * dt
        self.rect.center = self.pos + self.offset.rotate(self.angle)
    
    def render(self, scroll):
        display.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

