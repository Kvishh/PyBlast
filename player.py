import pygame
from configs import *
from game_map import tiles

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.transform.scale(pygame.image.load("assets/images/main_sorcerer.png").convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.orientation = {1: self.image, -1: pygame.transform.flip(self.image, True, False)}
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.x_velocity = 0
        self.y_velocity = 0
        self.jumping = False
        self.x_direction = 1

    def update(self, keys, dt):
        self.image = self.orientation[self.x_direction]
        self._move(keys)

        # this is for checking whether enemy is stuck below or above
        self.vertical_rect = pygame.Rect(self.rect.centerx-10, 0, 20, 700)
        # pygame.draw.rect(display, (255, 0, 0), self.vertical_rect, 2) # original
        
        if self.y_velocity > 3000: self.y_velocity = 3000

        # Border limit x
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > WINDOW_WIDTH - PLAYER_WIDTH:
            self.pos.x = WINDOW_WIDTH - PLAYER_WIDTH
        # Border limit y
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > WINDOW_HEIGHT - PLAYER_HEIGHT:
            self.y_velocity = 0
            self.pos.y = FLOOR - PLAYER_HEIGHT
        
        # Responsible for x movement
        if int(self.x_velocity) == 0:
            self.x_velocity == 0
        elif self.x_velocity > 0:
            self.x_velocity -= FRICTION
        elif self.x_velocity < 0:
            self.x_velocity += FRICTION
        self.pos.x += self.x_velocity * dt
        self.rect.x = int(self.pos.x)
        
        self._detect_tiles_collision_x()

        # Responsible for y movement
        self.y_velocity += GRAVITY * dt * .8
        self.pos.y += self.y_velocity * dt * .8
        self.rect.y = int(self.pos.y)
        self.y_velocity += GRAVITY * dt * .8

        self._detect_tiles_collision_y()

    def render(self, scroll):
        display.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))
    
    def _move(self, keys_hold):
        if keys_hold[pygame.K_SPACE] and not self.jumping:
            self.y_velocity = -1170 # ORIGINAL 1050
            self.jumping = True
        elif keys_hold[pygame.K_d]:
            self.x_velocity = 350
            self.x_direction = 1
        elif keys_hold[pygame.K_a]:
            self.x_velocity = -350
            self.x_direction = -1

    def _get_tile_collision(self):
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                return tile
        return None

    def _detect_tiles_collision_x(self):
        tile = self._get_tile_collision()
        if tile is not None:
            if self.x_velocity > 0:
                self.pos.x = tile.rect.left - PLAYER_WIDTH
                self.rect.x = int(self.pos.x)
            elif self.x_velocity < 0:
                self.pos.x = tile.rect.right
                self.rect.x = int(self.pos.x)
            self.x_velocity = 0

    def _detect_tiles_collision_y(self):
        tile = self._get_tile_collision()
        if tile is not None:
            if self.y_velocity > 0:
                self.pos.y = tile.rect.top - PLAYER_HEIGHT
                self.rect.y = int(self.pos.y)
                self.jumping = False
            elif self.y_velocity < 0:
                self.pos.y = tile.rect.bottom
                self.rect.y = int(self.pos.y)
            self.y_velocity = 0