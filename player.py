import pygame
from configs import *
from game_map import tiles

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.transform.scale(pygame.image.load("assets/images/megaman-right-walk0.png").convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.x_velocity = 0
        self.y_velocity = 0
        self.jumping = False
        self.x_direction = 1

    def update(self):
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
            self.pos.y = WINDOW_HEIGHT - PLAYER_HEIGHT
        
        # Responsible for x movement
        if self.x_velocity > 0:
            self.x_velocity -= 1
        elif self.x_velocity < 0:
            self.x_velocity += 1
        self.pos.x += self.x_velocity
        self.rect.x = int(self.pos.x)
        
        self._detect_tiles_collision_x()

        # Responsible for y movement
        self.y_velocity += GRAVITY
        self.pos.y += self.y_velocity
        self.rect.y = int(self.pos.y)

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