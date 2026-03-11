import pygame, math, random
from configs import *
from game_map import tiles
from enemy_bullet import EnemyBullet
from images import BurstImage

class Burst(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = BurstImage.burst_image_scaled
        self.rect = self.image.get_rect()
        self.orig_image = self.image
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 30

        self.hit_rect = pygame.Rect(0, 0, 62, 62)
        self.hit_rect.center = self.rect.center

        self.previous_time = pygame.time.get_ticks()
        self.previous_time_slowing_down = pygame.time.get_ticks()

        self.vel = pygame.Vector2(0, 0)

        self.seek_force = pygame.Vector2(0, 0)
        self.avoid_force = pygame.Vector2(0, 0)

        self.flee_rad = 60

        self.shoot_count = 0
        self.shot_interval = pygame.time.get_ticks()

        self.particles = []

    def update(self, enemy_bullet_group, all_bullets_group, pl, dt, flying_enemies_group, scroll):
        # pygame.draw.rect(display, (255, 0, 0), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.w, self.rect.h), 1)
        # pygame.draw.line(display, (0, 255, 0), (self.rect.centerx-scroll[0], self.rect.centery-scroll[1]), (pl.rect.midbottom[0]-scroll[0], pl.rect.midbottom[1]-scroll[1]), 2)
        self._draw_particles(scroll)

        self.rotate_sprite(pl)

        self.shoot(enemy_bullet_group, all_bullets_group, pl)

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
        elif self.rect.left > WINDOW_WIDTH - BURST_ENEMY_WIDTH:
            self.rect.left = WINDOW_WIDTH - BURST_ENEMY_WIDTH
        
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = WINDOW_HEIGHT
        elif self.rect.y < 0:
            self.rect.y = 0
        
        self.hit_rect.centerx = int(self.pos.x)
        self._detect_tiles_collision_x()

        self.hit_rect.centery = int(self.pos.y)
        self._detect_tiles_collision_y()

        self.rect.center = self.hit_rect.center

    def shoot(self, enemy_bullet_group, all_bullets_group, player):
        current_time = pygame.time.get_ticks()

        if current_time - self.previous_time_slowing_down > 3000:
            self.speed -= .5
        else:
            self.speed += .5 if self.speed < 30 else 0

        if current_time - self.previous_time > 5000:
                if self.shoot_count < 3 and current_time - self.shot_interval > 1000:
                    self.shot_interval = current_time

                    target_x = player.rect.centerx
                    target_y = player.rect.centery

                    bullet = EnemyBullet(self.rect.centerx, 
                                    self.rect.centery, 
                                    1, 
                                    target_x,
                                    target_y)
                    enemy_bullet_group.add(bullet)
                    all_bullets_group.add(bullet)

                    self.shoot_count += 1
                    self.speed = 15

                elif self.shoot_count >= 3:
                    self.previous_time_slowing_down = current_time
                    self.previous_time = current_time
                    self.shoot_count = 0

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

    def _draw_particles(self, scroll):
        for i, particle in enumerate(self.particles):
            pygame.draw.circle(display, (23, 4, 23), (particle[0][0]-scroll[0]+4, particle[0][1]-scroll[1]+4), (i//3+2))
            pygame.draw.circle(display, particle[2], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), (i//3+2))

    def rotate_sprite(self, player):
        target_x = player.rect.centerx
        target_y = player.rect.centery
        dx = target_x - self.pos.x
        dy = target_y - self.pos.y
        angle = math.degrees(math.atan2(dy, dx))


        dir = angle%360

        if dir > -90 and dir < 90:
            self.angle_direction = 1
        elif dir >= -180 and dir <= 180:
            self.angle_direction = -1

        ########## TRAIL PARTICLE ##########
        for particle in self.particles:
            particle[0][0] -= particle[1][0]
            particle[0][1] += particle[1][1]
        
        vx = -math.cos(math.radians(angle)) * random.uniform(-3,3) + random.uniform(-0.5,0.5)
        vy = -math.sin(math.radians(angle)) * random.uniform(-3,3) + random.uniform(-0.5,0.5)

        if self.angle_direction > 0: particle = [[self.rect.center[0], self.rect.center[1]], [vx, vy], (122, random.randrange(37, 67), 120)]
        if self.angle_direction < 0: particle = [[self.rect.center[0]+1, self.rect.center[1]], [vx, vy], (122, random.randrange(37, 67), 120)]

        self.particles.append(particle)
        if len(self.particles) > 20:
            self.particles.pop(0)
        ########## TRAIL PARTICLE ##########


        self.image = pygame.transform.rotate(self.orig_image, -angle)
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))

    def get_tile_collided(self):
        for tile in tiles:
            if tile.rect.colliderect(self.hit_rect):
                return tile
        return None

    def _detect_tiles_collision_x(self):
        collided_tile = self.get_tile_collided()
        if collided_tile is not None:
            if self.x_vel > 0:
                self.pos.x = collided_tile.rect.left - self.hit_rect.width // 2
            elif self.x_vel < 0:
                self.pos.x = collided_tile.rect.right + self.hit_rect.width // 2
            self.hit_rect.centerx = int(self.pos.x)

    def _detect_tiles_collision_y(self):
        collided_tile = self.get_tile_collided()
        if collided_tile is not None:
            if self.y_vel > 0:
                self.pos.y = collided_tile.rect.top - self.hit_rect.height // 2
            elif self.y_vel < 0:
                self.pos.y = collided_tile.rect.bottom + self.hit_rect.height // 2
            self.hit_rect.centery = int(self.pos.y)