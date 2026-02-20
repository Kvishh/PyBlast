import pygame

class CustomGroup(pygame.sprite.Group):
    def draw(self, surface, scroll):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, (spr.rect.x-scroll[0], spr.rect.y-scroll[1]))
            # pygame.draw.rect(surface, (255, 0, 0), ((spr.rect.x-scroll[0], spr.rect.y-scroll[1]), (spr.rect.w, spr.rect.h)), width=2)
        self.lostsprites = []