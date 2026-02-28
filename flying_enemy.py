import pygame, math
from configs import *
from game_map import tiles

class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.transform.scale(pygame.image.load("assets/images/flight.png").convert_alpha(), (FLIGHT_ENEMY_WIDTH, FLIGHT_ENEMY_HEIGHT))
        self.orientation = {1: self.image, -1: pygame.transform.flip(self.image, True, False)}
        self.rect = self.image.get_rect()
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 40
        self.x_direction = 1

        self.vel = pygame.Vector2(0, 0)

        self.seek_force = pygame.Vector2(0, 0)
        self.avoid_force = pygame.Vector2(0, 0)

        self.flee_rad = 60

    def update(self, pl, dt, flying_enemies_group):
        self.switch_orientation()
        self.image = self.orientation[self.x_direction]

        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
        self.seek_force = self.seek(pl)
        self.avoid_force = self.flee(flying_enemies_group)
        self.vel += ((self.seek_force * 2) + (self.avoid_force * 3))

        if self.vel.length() > 5:
            self.vel.scale_to_length(5)

        self.x_vel, self.y_vel = self.vel.x * dt * self.speed, self.vel.y * dt * self.speed

        self.pos.x += self.x_vel
        self.pos.y += self.y_vel

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.left > WINDOW_WIDTH - FLIGHT_ENEMY_WIDTH:
            self.rect.left = WINDOW_WIDTH - FLIGHT_ENEMY_WIDTH
        
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = WINDOW_HEIGHT
        elif self.rect.y < 0:
            self.rect.y = 0
        
        self.rect.centerx = int(self.pos.x)
        self._detect_tiles_collision_x()

        self.rect.centery = int(self.pos.y)
        self._detect_tiles_collision_y()

    def render(self, scroll):
        display.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))        

    def seek(self, player):
        desired = (player.pos - self.pos).normalize() * 5

        steer = desired - self.vel
        if steer.length() > .2:
            steer.scale_to_length(.2)

        return steer

    def flee(self, flying_enemies_group):
        steer = pygame.Vector2(0, 0)
        for flying_enemy in flying_enemies_group.sprites():
            if flying_enemy is not self:
                dist = self.pos - flying_enemy.pos
                if dist.length() < self.flee_rad:
                    self.desired = dist.normalize() * 5
                    steer = self.desired - self.vel
                else:
                    self.desired = dist.normalize() * 5
                if steer.length() > .6:
                    steer.scale_to_length(.6)

        return steer

    def switch_orientation(self):
        if self.x_vel < 0:
            self.x_direction = -1
        elif self.x_vel > 0:
            self.x_direction = 1

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