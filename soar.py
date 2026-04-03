import pygame, random
from configs import *
from game_map import tiles_blocks
from images import SoarImage

class Soar(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = SoarImage.soar_image_scaled
        self.orientation = {1: self.image, -1: SoarImage.soar_image_scaled_flipped}
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 20
        self.x_direction = 1

        self.vel = pygame.Vector2(0, 0)

        self.image_flashed_white = SoarImage.soar_image_flashed_white_scaled
        self.image_flashed_white_right = SoarImage.soar_image_flashed_white_scaled_flipped
        self.flashed_white_orientation = {1: self.image_flashed_white, -1: self.image_flashed_white_right}

        self.is_hit = False
        self.flashed_timer = 0
        self.flashed_duration = 210

        self.hp = 45

        self.tiles_collision_offset = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
                                       (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                                       (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
                                       (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                                       (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2)]

        self.seek_force = pygame.Vector2(0, 0)
        self.avoid_force = pygame.Vector2(0, 0)

        self.flee_rad = 60

        self.particles = []

    def update(self, pl, dt, flying_enemies_group, scroll):
        self.switch_orientation()
        self.mask = pygame.mask.from_surface(self.image)

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
        elif self.rect.left > WINDOW_WIDTH - SOAR_ENEMY_WIDTH:
            self.rect.left = WINDOW_WIDTH - SOAR_ENEMY_WIDTH
        
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
                    self.desired = dist.normalize() * 5 if dist.length() > 0.1 else pygame.Vector2(1, 1)
                    steer = self.desired - self.vel
                else:
                    self.desired = dist.normalize() * 5
                if steer.length() > .6:
                    steer.scale_to_length(.6)

        return steer

    def create_particles(self):
        if len(self.particles) < 20: # loc, velocity, radius, color
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

                particle[2] -= .2
                pygame.draw.circle(display, (48, 18, 56), (particle[0][0]-scroll[0]+4, particle[0][1]-scroll[1]+4), particle[2])
                pygame.draw.circle(display, particle[3], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), particle[2])

    def switch_orientation(self):
        if self.x_vel < 0:
            self.x_direction = -1
            self.image = self.orientation[self.x_direction]
        elif self.x_vel > 0:
            self.x_direction = 1
            self.image = self.orientation[self.x_direction]
        
        if self.is_hit:
            if pygame.time.get_ticks() - self.flashed_timer > self.flashed_duration:
                self.is_hit = False

            self.image = self.flashed_white_orientation[self.x_direction]
        


    def get_tile_collided(self):
        tiles_loc = []
        collided_tiles = []

        player_tile_loc = (int(self.rect.x // TILE_SIZE), int(self.rect.y // TILE_SIZE))

        for offset in self.tiles_collision_offset:
            check_loc = str(player_tile_loc[0] + offset[0]) + ";" + str(player_tile_loc[1] + offset[1])
            if check_loc in tiles_blocks:
                tiles_loc.append(check_loc)
        
        for tile in tiles_loc:
            collided_tiles.append(tiles_blocks[tile])

        return collided_tiles

    def _detect_tiles_collision_x(self):
        collided_tiles = self.get_tile_collided()
        for collided_tile in collided_tiles:
            if collided_tile.rect.colliderect(self.rect):
                if self.x_vel > 0:
                    self.rect.right = collided_tile.rect.left
                elif self.x_vel < 0:
                    self.rect.left = collided_tile.rect.right
                self.pos.x = pygame.Vector2(self.rect.center).x

    def _detect_tiles_collision_y(self):
        collided_tiles = self.get_tile_collided()
        for collided_tile in collided_tiles:
            if collided_tile.rect.colliderect(self.rect):
                if self.y_vel > 0:
                    self.rect.bottom = collided_tile.rect.top
                elif self.y_vel < 0:
                    self.rect.top = collided_tile.rect.bottom
                self.pos.y = pygame.Vector2(self.rect.center).y