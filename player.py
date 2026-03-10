import pygame, random
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
        self.on_ground = False
        self.x_direction = 1

        self.dust_particles = []

        self.gradient_image = pygame.transform.scale(pygame.image.load("assets/images/radial_gradient.png").convert(), (270, 270))
        self.gradient_layers = pygame.Surface((155,155))
        self.gradient_layers.set_colorkey((0,0,0))

        self.idle_count = 0
        self.idle_animation_update = pygame.time.get_ticks()
        self.idle_animations_frames_list = self.load_animation("assets/images/player_animation_idle.png", 1, 2, 21, 24)
        self.idle_animations_frames_list_left = [pygame.transform.flip(frame, True, False) for frame in self.idle_animations_frames_list]

        self.run_count = 0
        self.run_animation_update = pygame.time.get_ticks()
        self.run_animations_frames_list = self.load_animation("assets/images/player_animation_run.png", 1, 3, 21, 24)
        self.run_animations_frames_list_left = [pygame.transform.flip(frame, True, False) for frame in self.run_animations_frames_list]

        self.max_hp = 4
        self.current_hp = 3
        self.shield = 2


    def update(self, keys, dt, jump_particles, dark_overlay, scroll):
        self.on_ground = False
        self.ground_test_rect = pygame.Rect(self.rect.midleft[0], self.rect.midbottom[1]+5, PLAYER_WIDTH, 3)

        self.draw_glow(dark_overlay, scroll)

        # checks if ground_test_rect is touching any tiles
        self.check_if_on_ground()

        self.update_image()
        self._move(keys, jump_particles)

        # this is for checking whether enemy is stuck below or above
        self.vertical_rect = pygame.Rect(self.rect.centerx-10, 0, 20, 700)
        # pygame.draw.rect(display, (255, 0, 0), self.vertical_rect, 2) # original

        self.create_dust_particles()
        self.draw_dust_particles(scroll)

        if self.y_velocity > 3000: self.y_velocity = 3000

        # display.blit(self.idle_animations_frames_list[0], (60-scroll[0], 60-scroll[1], self.idle_animations_frames_list[0].get_rect().w, self.idle_animations_frames_list[0].get_rect().h))
        # display.blit(self.idle_animations_frames_list[1], (100-scroll[0], 60-scroll[1], self.idle_animations_frames_list[1].get_rect().w, self.idle_animations_frames_list[1].get_rect().h))

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

    def draw_glow(self, dark_overlay, scroll):
        # pygame.draw.rect(display,(255,0,0),(self.rect.x-scroll[0],self.rect.y-scroll[1],self.rect.w,self.rect.h),2)
        dark_overlay.blit(self.gradient_image,
                                (self.rect.x - scroll[0] - ((self.rect.w*2) + 32),
                                self.rect.y - scroll[1] - (self.rect.h*2)),
                                special_flags=pygame.BLEND_RGBA_ADD)
        
        for i in range(2, 0, -1):
            c = 35 - (i*15)
            c = pygame.math.clamp(c, 5, 255)
            r = 30 + (i*20) + 8
            pygame.draw.circle(self.gradient_layers, (c,c,c), self.gradient_layers.get_rect().center, r)

        display.blit(self.gradient_layers,
                        ((self.rect.x - scroll[0]) - ((self.gradient_layers.get_rect().w//2) - 19),
                        (self.rect.y - scroll[1]) - ((self.gradient_layers.get_rect().h//2)) + 25),
                        special_flags=pygame.BLEND_RGBA_ADD)

    def update_idle_animation(self):
        now = pygame.time.get_ticks()
        if now - self.idle_animation_update > 250:
            self.idle_animation_update = now
            self.idle_count = (self.idle_count + 1) % len(self.idle_animations_frames_list)

    def update_run_animation(self):
        now = pygame.time.get_ticks()
        if now - self.run_animation_update > 150:
            self.run_animation_update = now
            self.run_count = (self.run_count + 1) % len(self.run_animations_frames_list)

    def load_animation(self, file, row, col, width, height):
        idle_pictures = []

        idle_spritesheet = pygame.image.load(file).convert_alpha()

        for i in range(row):
            for j in range(col):
                x = j * width # 21 is frame width for player idle
                y = i * height # 24 is frame height for player idle
                frame = idle_spritesheet.subsurface((x, y, width, height))
                frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
                idle_pictures.append(frame)
        
        return idle_pictures

    def update_image(self):
        self.image = self.orientation[self.x_direction]
        if self.x_velocity == 0:
            if self.x_direction > 0:
                self.image = self.idle_animations_frames_list[self.idle_count]
            else: 
                self.image = self.idle_animations_frames_list_left[self.idle_count]
            self.update_idle_animation()


        elif self.x_velocity != 0:
            if self.x_direction > 0:
                self.image = self.run_animations_frames_list[self.run_count]
            elif self.x_direction < 0:
                self.image = self.run_animations_frames_list_left[self.run_count]
            self.update_run_animation()

    def check_if_on_ground(self):
        for tile in tiles:
            if tile.rect.colliderect(self.ground_test_rect):
                self.on_ground = True

    def _move(self, keys_hold, jump_particles):
        if keys_hold[pygame.K_SPACE] and not self.jumping and self.on_ground:
            self.y_velocity = -1170 # ORIGINAL 1050
            self.jumping = True
            for _ in range(3): # location, y_velocity, radius
                jump_particles.append([[random.randrange(self.rect.midbottom[0]-5, self.rect.midbottom[0]+5), self.rect.midbottom[1]],
                                       [random.randrange(-2, 2), 2],
                                       random.randrange(5, 8)]) 
        elif keys_hold[pygame.K_d]:
            self.x_velocity = 350
            self.x_direction = 1
        elif keys_hold[pygame.K_a]:
            self.x_velocity = -350
            self.x_direction = -1

    def create_dust_particles(self):
        if self.x_velocity != 0 and not self.jumping and self.y_velocity < 500:
                if len(self.dust_particles) < 30:# loc, radius, velocity
                    self.dust_particles.append([[self.rect.midbottom[0], self.rect.midbottom[1]],
                                5,
                                [random.randint(-2, 2), random.randint(-15, 0)*.1]])

    def draw_dust_particles(self, scroll):
        if self.dust_particles:# loc, radius, velocity
            self.dust_particles = [dust for dust in self.dust_particles if dust[1] > 0]

            for dust in self.dust_particles:
                dust[0][0] -= dust[2][0]
                dust[0][1] += dust[2][1]
                dust[1] -= .2

                pygame.draw.circle(display,
                                (23, 14, 71),
                                (dust[0][0]-scroll[0]+4, dust[0][1]-scroll[1]+4),
                                int(dust[1]))

                pygame.draw.circle(display,
                                (random.randrange(160, 180), random.randint(175, 185), 204),
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