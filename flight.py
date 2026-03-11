import pygame, math, random
from configs import *
from game_map import tiles
from images import FlightImage

class Flight(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = FlightImage.flight_image_scaled
        self.orientation = {1: self.image, -1: FlightImage.flight_image_scaled_flipped}
        self.rect = self.image.get_rect()
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 35
        self.x_direction = 1

        self.vel = pygame.Vector2(0, 0)

        self.seek_force = pygame.Vector2(0, 0)
        self.avoid_force = pygame.Vector2(0, 0)

        self.flee_rad = 60

        self.particles = []

        self.animation_count = 0
        self.animation_update = pygame.time.get_ticks()
        self.animations_frames_list = FlightImage.flight_run_animations_frames_list
        self.animations_frames_list_right = FlightImage.flight_run_animations_frames_flipped_list

    def update(self, pl, dt, flying_enemies_group, scroll):
        self.switch_orientation()
        self.image = self.orientation[self.x_direction]
        self.update_image()


        self.create_particles()
        self._draw_particles(scroll)

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

    def update_image(self):
        if self.x_direction > 0:
            self.image = self.animations_frames_list[self.animation_count]
        else:
            self.image = self.animations_frames_list_right[self.animation_count]
        self.update_animation()

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.animation_update > 250:
            self.animation_update = now
            self.animation_count = (self.animation_count + 1) % len(self.animations_frames_list)

    def create_particles(self):
        if len(self.particles) < 15: # loc, velocity, radius, color
            self.particles.append([[self.rect.centerx, self.rect.centery],
                                   [random.randint(1, 3), random.uniform(-2, 2)],
                                   10,
                                   (122, random.randrange(37, 67), 120)])

    def _draw_particles(self, scroll):
        if self.particles:
            self.particles = [particle for particle in self.particles if particle[2] > 4]

            for particle in self.particles:
                if self.x_direction > 0: particle[0][0] -= particle[1][0]
                if self.x_direction < 0: particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]

                particle[2] -= .3
                pygame.draw.circle(display, (48, 18, 56), (particle[0][0]-scroll[0]+4, particle[0][1]-scroll[1]+4), particle[2])
                pygame.draw.circle(display, particle[3], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), particle[2])

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
                    self.desired = dist.normalize() * 5 if dist.length() > 0.1 else pygame.Vector2(1, 1)
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