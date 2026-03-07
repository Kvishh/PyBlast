import pygame, random
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

        self.dust_particles = []

        self.animation_count = 0
        self.animation_update = pygame.time.get_ticks()
        self.animations_frames_list = self.load_animation("assets/images/tank_animation.png", 1, 3, 28, 32)
        self.animations_frames_list_right = [pygame.transform.flip(frame, True, False) for frame in self.animations_frames_list]

    def update(self, dt, player, scroll):
        self.image = self.orientation[self.x_direction]
        self.update_image()
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

        self.create_dust_particles()
        self.draw_dust_particles(scroll)

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

    def load_animation(self, file, row, col, width, height):
        idle_pictures = []

        idle_spritesheet = pygame.image.load(file).convert_alpha()

        for i in range(row):
            for j in range(col):
                x = j * width # 21 is frame width for player idle
                y = i * height # 24 is frame height for player idle
                frame = idle_spritesheet.subsurface((x, y, width, height))
                frame = pygame.transform.scale(frame, (HEAVY_ENEMY_WIDTH, HEAVY_ENEMY_HEIGHT))
                idle_pictures.append(frame)
        
        return idle_pictures

    def create_dust_particles(self):
        if self.x_velocity != 0 and not self.jumping and self.y_velocity < 500:
                if len(self.dust_particles) < 15: # loc, radius, velocity, color
                    colors = random.choice([(random.randrange(160, 180), random.randint(175, 185), 204),
                                            (random.randrange(224, 232), random.randint(38, 68), 255)])
                    self.dust_particles.append([[self.rect.midbottom[0], self.rect.midbottom[1]-6],
                                5,
                                [random.randint(-2, 2), random.randint(-10, 0)*.1],
                                colors])

    def draw_dust_particles(self, scroll):
        if self.dust_particles:# loc, radius, velocity, color
            self.dust_particles = [dust for dust in self.dust_particles if dust[1] > 0]

            for dust in self.dust_particles:
                dust[0][0] -= dust[2][0]
                dust[0][1] += dust[2][1]
                dust[1] -= .1

                pygame.draw.circle(display,
                                (23, 14, 71),
                                (dust[0][0]-scroll[0]+4, dust[0][1]-scroll[1]+4),
                                int(dust[1]))

                pygame.draw.circle(display,
                                dust[3],
                                (dust[0][0]-scroll[0], dust[0][1]-scroll[1]),
                                int(dust[1]))

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