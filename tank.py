import pygame
from configs import *
from game_map import tiles

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.transform.scale(pygame.image.load("assets/images/tank.png").convert_alpha(), (HEAVY_ENEMY_WIDTH, HEAVY_ENEMY_HEIGHT))
        self.orientation = {1: self.image, -1: pygame.transform.flip(self.image, True, False)}
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.x_velocity = 100
        self.y_velocity = 0
        self.jumping = False
        self.x_direction = -1


    def update(self, dt, player):
        self.image = self.orientation[self.x_direction]
        # Border limit x
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > WINDOW_WIDTH - HEAVY_ENEMY_WIDTH:
            self.pos.x = WINDOW_WIDTH - HEAVY_ENEMY_WIDTH

        # Border limit y
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > WINDOW_HEIGHT - HEAVY_ENEMY_HEIGHT:
            self.y_velocity = 0
            self.pos.y = FLOOR - HEAVY_ENEMY_HEIGHT

        # Follow player
        ##################################
        if player.rect.centerx < self.rect.centerx:
            self.x_direction = 1
            self.x_velocity = -100
        elif player.rect.centerx > self.rect.centerx:
            self.x_direction = -1
            self.x_velocity = 100
        ##################################

        self.pos.x += self.x_velocity * dt
        self.rect.x = int(self.pos.x)

        self._detect_tiles_collision_x()

        self.y_velocity += GRAVITY * dt * .8
        self.pos.y += self.y_velocity * dt * .8
        self.rect.y = int(self.pos.y)
        self.y_velocity += GRAVITY * dt * .8

        self._detect_tiles_collision_y()

    def render(self, scroll):
        display.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

    def _get_tile_collision(self):
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                return tile
        return None

    def _detect_tiles_collision_x(self):
        tile = self._get_tile_collision()
        if tile is not None:
            if self.x_velocity > 0:
                self.pos.x = tile.rect.left - HEAVY_ENEMY_WIDTH
                self.rect.x = int(self.pos.x)
            elif self.x_velocity < 0:
                self.pos.x = tile.rect.right
                self.rect.x = int(self.pos.x)
            self.x_velocity = 0

    def _detect_tiles_collision_y(self):
        tile = self._get_tile_collision()
        if tile is not None:
            if self.y_velocity > 0:
                self.pos.y = tile.rect.top - HEAVY_ENEMY_HEIGHT
                self.rect.y = int(self.pos.y)
                self.jumping = False
            elif self.y_velocity < 0:
                self.pos.y = tile.rect.bottom
                self.rect.y = int(self.pos.y)
            self.y_velocity = 0