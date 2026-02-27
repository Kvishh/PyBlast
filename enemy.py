import pygame
from configs import *
from game_map import tiles

class Light(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("assets/images/slime.png").convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)
        self.orientation = {1: self.image, -1: pygame.transform.flip(self.image, True, False)}        
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.x_velocity = 120
        self.y_velocity = 0
        self.jumping = False
        self.x_direction = 0

        self.sensor = pygame.Rect(0, 0, PLAYER_WIDTH+80, 80)
        self.stuck = False
        self.stuck_center_posx = 0

        self.stuck_rect_collision_count = 0
    
    def update(self, dt, player):
        self.switch_orientation(player)
        self.image = self.orientation[self.x_direction]

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


        self.sensor.center = (self.rect.x+20, self.rect.centery - PLAYER_HEIGHT)
        # pygame.draw.rect(display, (255, 255, 255), ((self.sensor.x-scroll[0], self.sensor.y-scroll[1]), (self.sensor.w, self.sensor.h)), 1)

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
            if self.stuck_center_posx <= (544 + (PLAYER_WIDTH // 2)) and self.rect.centerx > MAP_HALF + 20:
                self.stuck = False
            elif self.stuck_center_posx > 685 and self.rect.centerx < MAP_HALF - 70:
                self.stuck = False
            elif (self.stuck_center_posx > (544 + (PLAYER_WIDTH // 2))) and (self.stuck_center_posx < (704 - (PLAYER_WIDTH // 2))) and self.rect.centerx < (363 - PLAYER_WIDTH*3):
                self.stuck = False
        
        # print(self.rect.centerx)
        if self.stuck and self.stuck_center_posx <= (544 + (PLAYER_WIDTH // 2)):
            self.x_velocity = 150
        elif self.stuck and self.stuck_center_posx > (704 - (PLAYER_WIDTH // 2)):
            self.x_velocity = -150
        elif self.stuck and self.stuck_center_posx > (544 + (PLAYER_WIDTH // 2)) and self.stuck_center_posx < (704 - (PLAYER_WIDTH // 2)):
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
        elif self.x_velocity > 0:
            self.x_direction = 1

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