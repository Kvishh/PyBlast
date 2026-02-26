import pygame, math
from configs import *
from game_map import tiles
from enemy_bullet import EnemyBullet

class ShootingEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.transform.scale(pygame.image.load("assets/images/blader-left.png").convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 150

        self.previous_time = pygame.time.get_ticks()
        self.previous_time_slowing_down = pygame.time.get_ticks()

    def update(self, enemy_bullet_group, all_bullets_group, pl, dt):
        # pygame.draw.rect(display, (255, 0, 0), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.w, self.rect.h), 1)
        # pygame.draw.line(display, (0, 255, 0), (self.rect.centerx-scroll[0], self.rect.centery-scroll[1]), (pl.rect.midbottom[0]-scroll[0], pl.rect.midbottom[1]-scroll[1]), 2)

        self.shoot(enemy_bullet_group, all_bullets_group, pl)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.left > WINDOW_WIDTH - PLAYER_WIDTH:
            self.rect.left = WINDOW_WIDTH - PLAYER_WIDTH
        
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = WINDOW_HEIGHT
        elif self.rect.y < 0:
            self.rect.y = 0
        
        dx = pl.rect.x - self.rect.x
        dy = pl.rect.y - self.rect.y
        dist = pygame.Vector2(dx, dy).length()

        if dist > 1:
            direction_vector = pygame.Vector2(dx, dy).normalize()
            self.x_vel = direction_vector.x * self.speed * dt
            self.y_vel = direction_vector.y * self.speed * dt
            
            self.pos += direction_vector * self.speed * dt
        else:
            self.x_vel = 0
            self.y_vel = 0
        
        self.rect.centerx = int(self.pos.x)
        self._detect_tiles_collision_x()

        self.rect.centery = int(self.pos.y)
        self._detect_tiles_collision_y()

    def shoot(self, enemy_bullet_group, all_bullets_group, player):
        current_time = pygame.time.get_ticks()
        self.slow_down()
        if current_time - self.previous_time > 5000:
                self.previous_time = current_time
                target_x = player.rect.centerx
                target_y = player.rect.centery

                bullet = EnemyBullet("assets/images/bullet.png", 
                                self.rect.centerx, 
                                self.rect.centery, 
                                1, 
                                target_x,
                                target_y)
                enemy_bullet_group.add(bullet)
                all_bullets_group.add(bullet)

                self.speed = 150
                self.previous_time_slowing_down = current_time

    def slow_down(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.previous_time_slowing_down > 3000:
            self.speed -= 2


    def render(self, scroll):
        display.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))        

    def get_tile_collided(self):
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                return tile
        return None

    def _detect_tiles_collision_x(self):
        collided_tile = self.get_tile_collided()
        if collided_tile is not None:
            if self.x_vel > 0:
                self.rect.right = collided_tile.rect.left
            elif self.x_vel < 0:
                self.rect.left = collided_tile.rect.right
            self.pos.x = pygame.Vector2(self.rect.center).x

    def _detect_tiles_collision_y(self):
        collided_tile = self.get_tile_collided()
        if collided_tile is not None:
            if self.y_vel > 0:
                self.rect.bottom = collided_tile.rect.top
            elif self.y_vel < 0:
                self.rect.top = collided_tile.rect.bottom
            self.pos.y = pygame.Vector2(self.rect.center).y