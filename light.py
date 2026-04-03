import pygame, random
from configs import *
from game_map import tiles_blocks
from images import LightImage

class Light(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = LightImage.light_image_scaled
        self.orientation = {1: self.image, -1: LightImage.light_image_scaled_flipped}
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.x_velocity = 120
        self.y_velocity = 0
        self.jumping = False
        self.x_direction = 0

        self.image_flashed_white = LightImage.light_image_flashed_white_scaled
        self.image_flashed_white_right = LightImage.light_image_flashed_white_scaled_flipped
        self.flashed_white_orientation = {1: self.image_flashed_white, -1: self.image_flashed_white_right}

        self.is_hit = False
        self.flashed_timer = 0
        self.flashed_duration = 210

        self.hp = 20

        self.tiles_collision_offset = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
                                (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                                (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
                                (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                                (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2)]

        self.sensor = pygame.Rect(0, 0, LIGHT_ENEMY_WIDTH+80, 80)
        self.stuck = False
        self.stuck_center_posx = 0

        self.stuck_rect_collision_count = 0

        self.dust_particles = []

    def update(self, dt, player, scroll, set_of_alive_enemies):
        self.switch_orientation(player)
        self.mask = pygame.mask.from_surface(self.image)

        # Border limit x
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > WINDOW_WIDTH - LIGHT_ENEMY_WIDTH:
            self.pos.x = WINDOW_WIDTH - LIGHT_ENEMY_WIDTH

        # Border limit y
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > WINDOW_HEIGHT - LIGHT_ENEMY_HEIGHT:
            self.y_velocity = 0
            # If enemy fell down, kill (remove from pygame.Group objects) and remove it in set_of_alive_enemies
            self.kill()
            set_of_alive_enemies.remove(self)


        self.sensor.center = (self.rect.x+20, self.rect.centery - LIGHT_ENEMY_HEIGHT)
        # pygame.draw.rect(display, (255, 255, 255), ((self.sensor.x-scroll[0], self.sensor.y-scroll[1]), (self.sensor.w, self.sensor.h)), 1)

        self.create_dust_particles()
        self.draw_dust_particles(scroll)

        self._detect_jump(player)
    
        # Follow player
        ##################################
        MAP_HALF = WINDOW_WIDTH//2

        if self.rect.y < player.rect.y: # if enemy is above player
            if player.rect.y == FLOOR:
                if player.rect.centerx < self.rect.centerx:
                    self.x_velocity = -150
                elif player.rect.centerx > self.rect.centerx:
                    self.x_velocity = 150

                self.check_if_stuck(player)

                if self.stuck_rect_collision_count > 20:
                    self.stuck = True
                    self.stuck_center_posx = self.rect.centerx

        elif self.rect.y > player.rect.y: # if enemy is below player
            if self.rect.y == FLOOR:
                if player.rect.centerx < self.rect.centerx:
                    self.x_velocity = -150
                elif player.rect.centerx > self.rect.centerx:
                    self.x_velocity = 150
                
                self.check_if_stuck(player)

                if self.stuck_rect_collision_count > 20:
                    self.stuck = True
                    self.stuck_center_posx = self.rect.centerx
            else:
                if player.rect.centerx < self.rect.centerx:
                    self.x_velocity = -150
                elif player.rect.centerx > self.rect.centerx:
                    self.x_velocity = 150
        else: # if both are equal, i.e. same y axis
            if self.rect.centerx < player.rect.centerx:
                self.x_velocity = 150
            elif self.rect.centerx > player.rect.centerx:
                self.x_velocity = -150

        # Checking if stuck
        # if self.stuck and self.rect.centerx >= 562 and self.rect.centerx <= 686:# and not self.stuck_in_below_middle_platform():
        #     self.stuck = False
        if self.stuck:
            if self.stuck_center_posx <= (544 + (LIGHT_ENEMY_WIDTH // 2)) and self.rect.centerx > MAP_HALF + 20:
                self.stuck = False
            elif self.stuck_center_posx > 685 and self.rect.centerx < MAP_HALF - 70:
                self.stuck = False
            elif (self.stuck_center_posx > (544 + (LIGHT_ENEMY_WIDTH // 2))) and (self.stuck_center_posx < (704 - (LIGHT_ENEMY_WIDTH // 2))) and self.rect.centerx < (363 - LIGHT_ENEMY_WIDTH*3):
                self.stuck = False
        
        # print(self.rect.centerx)
        if self.stuck and self.stuck_center_posx <= (544 + (LIGHT_ENEMY_WIDTH // 2)):
            self.x_velocity = 150
        elif self.stuck and self.stuck_center_posx > (704 - (LIGHT_ENEMY_WIDTH // 2)):
            self.x_velocity = -150
        elif self.stuck and self.stuck_center_posx > (544 + (LIGHT_ENEMY_WIDTH // 2)) and self.stuck_center_posx < (704 - (LIGHT_ENEMY_WIDTH // 2)):
            self.x_velocity = -150

        
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

    def switch_orientation(self, player):
        if self.x_velocity < 0:
            self.x_direction = -1
            self.image = self.orientation[self.x_direction]
        elif self.x_velocity > 0:
            self.x_direction = 1
            self.image = self.orientation[self.x_direction]

        if self.is_hit:
            if pygame.time.get_ticks() - self.flashed_timer > self.flashed_duration:
                self.is_hit = False

            self.image = self.flashed_white_orientation[self.x_direction]

    def _detect_jump(self, player):
        is_going_right = player.rect.centerx > self.rect.centerx
        is_going_left = player.rect.centerx < self.rect.centerx

        # If enemy at second row of platforms (i.e. two platforms above floor)
        if self.rect.centery == 520 and self.rect.y > player.rect.y:
            # If at 1st platform of two platfroms just above the floor jumping to platforms above
            if is_going_right and (self.rect.centerx > 470 and self.rect.centerx < 477):
                self.y_velocity = -1170
                self.jumping = True
            elif is_going_left and (self.rect.centerx > 458 and self.rect.centerx < 464):
                self.y_velocity = -1170
                self.jumping = True
            # If at 2nd platform of two platfroms just above the floor jumping to platforms above
            elif is_going_right and (self.rect.centerx > 785 and self.rect.centerx < 790):
                self.y_velocity = -1170
                self.jumping = True
            elif is_going_left and (self.rect.centerx > 777 and self.rect.centerx < 780):
                self.y_velocity = -1170
                self.jumping = True
        # If enemy on floor
        elif self.rect.y == FLOOR and self.rect.y > player.rect.y:
            # If on floor and and jumping to 1st platform just above the floor
            if is_going_right and (self.rect.centerx > 312 and self.rect.centerx < 317):
                self.y_velocity = -1170
                self.jumping = True
            if is_going_left and (self.rect.centerx > 614 and self.rect.centerx < 618):
                self.y_velocity = -1170
                self.jumping = True
            # If on floor and and jumping to 2nd platform just above the floor
            if is_going_right and (self.rect.centerx > 628 and self.rect.centerx < 635):
                self.y_velocity = -1170
                self.jumping = True
            if is_going_left and (self.rect.centerx > 934 and self.rect.centerx < 938):
                self.y_velocity = -1170
                self.jumping = True
        # If enemy on the platforms above the platforms just above the floor
        elif self.rect.centery == 392 and self.rect.y > player.rect.y:
            if is_going_left and (self.rect.centerx > 292 and self.rect.centerx < 297):
                self.y_velocity = -1170
                self.jumping = True
            elif is_going_right and (self.rect.centerx > 950 and self.rect.centerx < 959):
                self.y_velocity = -1170
                self.jumping = True

    def check_if_stuck(self, player):
        if self.rect.colliderect(player.vertical_rect):
            self.stuck_rect_collision_count += 1
        else: 
            self.stuck_rect_collision_count = 0    

    def create_dust_particles(self):
        if self.x_velocity != 0 and not self.jumping and self.y_velocity < 500:
                if len(self.dust_particles) < 15: # loc, radius, velocity, color
                    colors = random.choice([(random.randrange(160, 180), random.randint(175, 185), 204),
                                            (random.randrange(185, 206), random.randint(48, 99), 255)])
                    self.dust_particles.append([[self.rect.midbottom[0], self.rect.midbottom[1]-8],
                                5,
                                [random.randint(-2, 2), random.randint(-10, 0)*.1],
                                colors])

    def draw_dust_particles(self, scroll):
        if self.dust_particles:# loc, radius, velocity, color
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
                                dust[3],
                                (dust[0][0]-scroll[0], dust[0][1]-scroll[1]),
                                int(dust[1]))

    def _get_tile_collision(self):
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
        collided_tiles = self._get_tile_collision()
        for tile in collided_tiles:
            if tile.rect.colliderect(self.rect):
                if self.x_velocity > 0:
                    self.pos.x = tile.rect.left - LIGHT_ENEMY_WIDTH
                    self.rect.x = int(self.pos.x)
                elif self.x_velocity < 0:
                    self.pos.x = tile.rect.right
                    self.rect.x = int(self.pos.x)
                self.x_velocity = 0

    def _detect_tiles_collision_y(self):
        collided_tiles = self._get_tile_collision()
        for tile in collided_tiles:
            if tile.rect.y == 672 and tile.image.get_alpha() == 0:
                pass
            elif tile.rect.colliderect(self.rect):
                if self.y_velocity > 0:
                    self.pos.y = tile.rect.top - LIGHT_ENEMY_HEIGHT
                    self.rect.y = int(self.pos.y)
                    self.jumping = False
                elif self.y_velocity < 0:
                    self.pos.y = tile.rect.bottom
                    self.rect.y = int(self.pos.y)
                self.y_velocity = 0