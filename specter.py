import pygame, math
from configs import *
from game_map import tiles_blocks
from enemy_bullet import SpecterEnemyBullet
from images import SpecterImage
from sound_system import SFX

class Specter(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = SpecterImage.specter_image_scaled
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.orig_image = self.image
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 20

        self.hit_rect = pygame.Rect(0, 0, 50, 50)
        self.hit_rect.center = self.rect.center

        self.flashed_white_image = SpecterImage.specter_flashed_white_image_scaled

        self.is_hit = False
        self.flashed_timer = 0
        self.flashed_duration = 210

        self.hp = 20

        self.tiles_collision_offset = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
                                    (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                                    (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
                                    (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                                    (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2)]

        self.previous_time = 0
        self.previous_time_slowing_down = 0
        self.current_time = 0

        self.vel = pygame.Vector2(0, 0)

        self.seek_force = pygame.Vector2(0, 0)
        self.avoid_force = pygame.Vector2(0, 0)

        self.flee_rad = 60

        self.allow_increase = True
        self.opacity = 255


    def update(self, specter_enemy_bullet_group, pl, dt, flying_enemies_group, all_enemy_projectiles_that_hit_player, enemy_shoot_sfx_count):
        # pygame.draw.rect(display, (255, 0, 0), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.w, self.rect.h), 1)
        # pygame.draw.line(display, (0, 255, 0), (self.rect.centerx-scroll[0], self.rect.centery-scroll[1]), (pl.rect.midbottom[0]-scroll[0], pl.rect.midbottom[1]-scroll[1]), 2)

        self.rotate_sprite(pl)

        self.shoot(specter_enemy_bullet_group, all_enemy_projectiles_that_hit_player, pl, dt, enemy_shoot_sfx_count)

        
        self.image.set_alpha(self.opacity)
        if self.allow_increase:
            self.opacity += 2 if self.opacity <= 253 else 0
        if self.is_hit: self.image.set_alpha(255)


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
        elif self.rect.left > WINDOW_WIDTH - SPECTER_ENEMY_WIDTH:
            self.rect.left = WINDOW_WIDTH - SPECTER_ENEMY_WIDTH
        
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = WINDOW_HEIGHT
        elif self.rect.y < 0:
            self.rect.y = 0
        
        self.hit_rect.centerx = int(self.pos.x)
        self._detect_tiles_collision_x()

        self.hit_rect.centery = int(self.pos.y)
        self._detect_tiles_collision_y()

        self.rect.center = self.hit_rect.center

    def shoot(self, specter_enemy_bullet_group, all_enemy_projectiles_that_hit_player, player, dt, enemy_shoot_sfx_count):
        self.current_time += dt
        self.slow_down()
        if self.current_time - self.previous_time > 3.3:
                if enemy_shoot_sfx_count[0] < 5:
                    SFX.enemies_bullet_fire_sfx.play()
                    enemy_shoot_sfx_count[0] += 1
                
                self.previous_time = self.current_time
                target_x = player.rect.centerx
                target_y = player.rect.centery

                bullet = SpecterEnemyBullet(self.rect.centerx, 
                                self.rect.centery, 
                                1, 
                                target_x,
                                target_y)
                specter_enemy_bullet_group.add(bullet)
                all_enemy_projectiles_that_hit_player.add(bullet)

                self.speed = 20
                self.previous_time_slowing_down = self.current_time
                self.allow_increase = True

    def slow_down(self):
        if self.current_time - self.previous_time_slowing_down > 1.5:
            self.speed = max(-20, self.speed - .3)
            self.opacity -= 2
            self.opacity = max(self.opacity, 30)
            self.allow_increase = False

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
                    self.desired = dist.normalize() * 5 if dist.length() > 0.1 else pygame.Vector2(1, 1)
                    steer = self.desired - self.vel
                else:
                    self.desired = dist.normalize() * 5
                if steer.length() > .6:
                    steer.scale_to_length(.6)

        return steer

    def render(self, scroll):
        display.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))        

    def rotate_sprite(self, player):
        target_x = player.rect.centerx
        target_y = player.rect.centery
        dx = target_x - self.pos.x
        dy = target_y - self.pos.y
        angle = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.orig_image, -angle)
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))
        self.mask = pygame.mask.from_surface(self.image)

        if self.is_hit:
            if pygame.time.get_ticks() - self.flashed_timer > self.flashed_duration:
                self.is_hit = False

            self.image = pygame.transform.rotate(self.flashed_white_image, -angle)

    def get_tile_collided(self):
        tiles_loc = []
        collided_tiles = []

        self_tile_loc = (int(self.hit_rect.x // TILE_SIZE), int(self.hit_rect.y // TILE_SIZE))

        for offset in self.tiles_collision_offset:
            check_loc = str(self_tile_loc[0] + offset[0]) + ";" + str(self_tile_loc[1] + offset[1])
            if check_loc in tiles_blocks:
                tiles_loc.append(check_loc)
        
        for tile in tiles_loc:
            collided_tiles.append(tiles_blocks[tile])

        return collided_tiles

    def _detect_tiles_collision_x(self):
        collided_tiles = self.get_tile_collided()
        for tile in collided_tiles:
            if tile.rect.colliderect(self.hit_rect):
                if self.x_vel > 0:
                    self.pos.x = tile.rect.left - self.hit_rect.width // 2
                elif self.x_vel < 0:
                    self.pos.x = tile.rect.right + self.hit_rect.width // 2
                self.hit_rect.centerx = int(self.pos.x)

    def _detect_tiles_collision_y(self):
        collided_tiles = self.get_tile_collided()
        for tile in collided_tiles:
            if tile.rect.colliderect(self.hit_rect):
                if self.y_vel > 0:
                    self.pos.y = tile.rect.top - self.hit_rect.height // 2
                elif self.y_vel < 0:
                    self.pos.y = tile.rect.bottom + self.hit_rect.height // 2
                self.hit_rect.centery = int(self.pos.y)