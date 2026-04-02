import pygame, random, math
from configs import *
from game_map import tiles_blocks
from images import PlayerImages, GradientImage
from bullet import PlayerBullet
from negator import Negator
from font_system import FontSystem as fs
from sound_system import SFX

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.image = PlayerImages.player_image_scaled
        self.orientation = {1: self.image, -1: PlayerImages.player_image_scaled_flipped}
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.x_velocity = 0
        self.y_velocity = 0
        self.jumping = False
        self.on_ground = False
        self.x_direction = 1

        self.is_shooting = False

        self.movement_speed = 350 # 350 start, 500 max
        self.bullet_number = 1
        self.bullet_pierce_number = 1
        self.bullet_bounce_number = 0
        self.bullet_speed = 400
        self.damage = 10

        self.bullet_size_doubled_activated = False
        self.bullets_explode_state = False
        self.negator_active = False
        self.slow_time_active = True

        self.negator = Negator(self.rect.center)

        self.slow_rect = pygame.Rect(self.rect.x - (180//2) + (self.rect.w//2), (self.rect.y - (180//2) + (self.rect.h//2)), 180, 180)
        
        self.max_hp = 4
        self.current_hp = 4
        self.max_shield = 0
        self.current_shield = 0

        self.shield_timer = pygame.time.get_ticks()

        self.shoot_previous_time = 0
        self.fire_rate = 700
        self.shooting_cd = self.fire_rate / 1000 #700 start, 300 max

        self.current_time = 0

        self.active_skills = set([])
        

        # [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2)]
        # [(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1)]
        # [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)]
        # [(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1)]
        # [(-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2)]
        self.tiles_collision_offset = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
                                       (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                                       (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
                                       (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                                       (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2)]

        self.dust_particles = []

        self.gradient_image = GradientImage.gradient_player_image_scaled
        self.gradient_layers = pygame.Surface((155,155))
        self.gradient_layers.set_colorkey((0,0,0))
        for i in range(2, 0, -1):
            c = 35 - (i*15)
            c = pygame.math.clamp(c, 5, 255)
            r = 30 + (i*20) + 8
            pygame.draw.circle(self.gradient_layers, (c,c,c), self.gradient_layers.get_rect().center, r)

        self.idle_count = 0
        self.idle_animation_update = pygame.time.get_ticks()
        self.idle_animations_frames_list = PlayerImages.player_idle_animations_frames_list
        self.idle_animations_frames_list_left = PlayerImages.player_idle_animations_frames_flipped_list

        self.run_count = 0
        self.run_animation_update = pygame.time.get_ticks()
        self.run_animations_frames_list = PlayerImages.player_run_animations_frames_list
        self.run_animations_frames_list_left = PlayerImages.player_run_animations_frames_flipped_list

        self.is_hit_current_timer = 0
        self.is_invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1.5

        self.blink_timer = 0
        self.blink_state = False

        self.current_timer = 0

        self.hurt_overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.hurt_overlay_alpha = 0

        self.dash_num = 0

        self.dash_particles = []
        self.text_surfs_alpha = 2

        self.died_text = fs.render_outlined("You Died!", (255,0,0), (0,0,0), 2, fs.died_header_font)
        self.died_text.set_alpha(self.text_surfs_alpha)

        self.survived_text = fs.render_outlined("You Survived!", (0,255,0), (0,0,0), 2, fs.died_header_font)
        self.survived_text.set_alpha(self.text_surfs_alpha)

        self.try_again_text_surf = fs.render_outlined("Try Again", (255,255,255), (0,0,0), 2, fs.header_font)
        self.try_again_text_pos = [(DISPLAY_WIDTH//2) - (self.try_again_text_surf.get_rect().w//2), 240]
        self.try_again_text_rect = self.try_again_text_surf.get_rect(topleft=(self.try_again_text_pos[0], self.try_again_text_pos[1]))
        self.try_again_text_surf.set_alpha(self.text_surfs_alpha)

        self.win_back_text_surf = fs.render_outlined("Back to Main Menu", (255,255,255), (0,0,0), 2, fs.header_font)
        self.win_back_text_pos = [(DISPLAY_WIDTH//2) - (self.win_back_text_surf.get_rect().w//2), 340]
        self.win_back_text_rect = self.win_back_text_surf.get_rect(topleft=(self.win_back_text_pos[0], self.win_back_text_pos[1]))
        self.win_back_text_surf.set_alpha(self.text_surfs_alpha)

        self.retry_text_surf = fs.render_outlined("Retry", (255,255,255), (0,0,0), 2, fs.skill_name_font)
        self.retry_text_pos = [30, 470]
        self.retry_text_rect = self.retry_text_surf.get_rect(topleft=(self.retry_text_pos[0], self.retry_text_pos[1]))
        self.retry_text_surf.set_alpha(self.text_surfs_alpha)

        self.back_text_surf = fs.render_outlined("Back to Main Menu", (255,255,255), (0,0,0), 2, fs.skill_name_font)
        self.back_text_pos = [30, 520]
        self.back_text_rect = self.back_text_surf.get_rect(topleft=(self.back_text_pos[0], self.back_text_pos[1]))
        self.back_text_surf.set_alpha(self.text_surfs_alpha)
    
        self.has_survived = False

        self.walk_timer = 0


    def update(self, keys, dt, dark_overlay, scroll, wand, jump_particles=None, player_bullet_group=None, alive=False):
        # Only update character if player is alive
        if self.alive() or alive:
            self.current_timer += dt

            if self.walk_timer > 0: self.walk_timer -= 1

            if self.slow_time_active:
                self.slow_rect = pygame.Rect(self.rect.x - (180//2) + (self.rect.w//2), (self.rect.y - (180//2) + (self.rect.h//2)), 180, 180)
                # pygame.draw.rect(display, (255,0,0), (self.slow_rect.x-scroll[0], self.slow_rect.y-scroll[1], self.slow_rect.w, self.slow_rect.h), 2)

            if self.negator_active:
                self.negator.update(self.rect.center, dt)
                self.negator.render(scroll)

            # For shield regeneration
            now = pygame.time.get_ticks()
            if now - self.shield_timer > 120000: # 2 mins
                self.shield_timer = now
                self.current_shield = min(self.current_shield+1, self.max_shield)

            self.on_ground = False
            self.ground_test_rect = pygame.Rect(self.rect.midleft[0], self.rect.midbottom[1]+5, PLAYER_WIDTH, 3)

            # Shoot bullets
            if not self.has_survived and player_bullet_group is not None:
                self.shoot_bullet(scroll, player_bullet_group, dt)

            # Check if player is hit
            self.player_is_hit(dt)

            # Draw the gradient circle behind player
            self.draw_glow(dark_overlay, scroll)

            # checks if ground_test_rect is touching any tiles
            self.check_if_on_ground()

            # Update animation image
            self.update_image()

            # Keys checking for movement
            if not self.has_survived and jump_particles is not None:
                self._move(keys, jump_particles)

            # this is for checking whether enemy is stuck below or above
            self.vertical_rect = pygame.Rect(self.rect.centerx-10, 0, 20, 700)
            # pygame.draw.rect(display, (255, 0, 0), self.vertical_rect, 2) # original
            
            # Creating and drawing of dust particles
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
                self.pos.x = (WINDOW_WIDTH // 2) - PLAYER_WIDTH
                self.pos.y = 365

                if not self.is_invincible:
                    self.current_hp -= 1
                    self.invincible_timer = self.current_timer
                    self.is_invincible = True
                    wand.invincible_timer = self.current_timer
                    wand.is_invincible = True
                    self.hurt_overlay_alpha = 92

            self.dash_num = max(0, self.dash_num - 1) if self.dash_num > 0 else min(0, self.dash_num + 1)
            
            # Apply dash movement independent of slow-time dt
            dash_applied = False
            if abs(self.dash_num) > 50:
                self.x_velocity = 18 if self.dash_direction > 0 else -18
                if abs(self.dash_num) == 51:
                    self.x_velocity *= 0.4 # Slow down at last frame of dash
                
                self._detect_tiles_collision_x()
                self.pos.x += self.x_velocity
                dash_applied = True
                self.create_dash_particles()
                
            if abs(self.dash_num) >= 45:
                self.image.set_alpha(0)
                self.is_invincible = True
            
            self.draw_dash_particles(scroll)

            # Apply normal movement only if not dashing
            if not dash_applied:
                if int(self.x_velocity) == 0:
                    self.x_velocity = 0
                elif self.x_velocity > 0:
                    self.x_velocity = max(0, self.x_velocity-FRICTION)
                elif self.x_velocity < 0:
                    self.x_velocity = min(0, self.x_velocity+FRICTION)
                self.pos.x += self.x_velocity * dt
            self.rect.x = int(self.pos.x)
            
            self._detect_tiles_collision_x()

            # Responsible for y movement
            if not dash_applied:
                self.y_velocity += GRAVITY * dt * .8
                self.pos.y += self.y_velocity * dt * .8
                self.rect.y = int(self.pos.y)
                self.y_velocity += GRAVITY * dt * .8

            self._detect_tiles_collision_y()

    def show_after_winning_options(self, events, retry):
        mx, my = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH), (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT)

        if self.text_surfs_alpha >= 255:
            for evt in events:
                if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                    if self.try_again_text_rect.collidepoint(mx, my):
                        retry[0] = True
                    elif self.win_back_text_rect.collidepoint(mx, my):
                        return False

        self.text_surfs_alpha = min(255, self.text_surfs_alpha+3)
        self.survived_text.set_alpha(self.text_surfs_alpha)
        self.try_again_text_surf.set_alpha(self.text_surfs_alpha)
        self.win_back_text_surf.set_alpha(self.text_surfs_alpha)

        self.try_again_text_pos[1] = max(220, self.try_again_text_pos[1]-2) if self.try_again_text_rect.collidepoint(mx, my) else min(240, self.try_again_text_pos[1]+2)

        self.win_back_text_pos[1] = max(320, self.win_back_text_pos[1]-2) if self.win_back_text_rect.collidepoint(mx, my) else min(340, self.win_back_text_pos[1]+2)

        display.blit(self.survived_text, ((DISPLAY_WIDTH//2) - (self.survived_text.get_rect().w//2), 50))
        display.blit(self.try_again_text_surf, (self.try_again_text_pos[0], self.try_again_text_pos[1]))
        display.blit(self.win_back_text_surf, (self.win_back_text_pos[0], self.win_back_text_pos[1]))

    def show_after_death_options(self, events, retry):
        mx, my = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH), (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT)
        
        # Only allowed click if options are fully visible
        if self.text_surfs_alpha >= 255:
            for evt in events:
                if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                    if self.retry_text_rect.collidepoint(mx, my):
                        retry[0] = True
                    elif self.back_text_rect.collidepoint(mx, my):
                        return False
        
        self.text_surfs_alpha = min(255, self.text_surfs_alpha+2)
        self.died_text.set_alpha(self.text_surfs_alpha)
        self.retry_text_surf.set_alpha(self.text_surfs_alpha)
        self.back_text_surf.set_alpha(self.text_surfs_alpha)

        # This is responsible for the text surfaces movement since
        # they move x when mouse hovers over them
        # Move right if it is being hovered over else go back to normal position
        self.retry_text_pos[0] = min(50, self.retry_text_pos[0]+2) if self.retry_text_rect.collidepoint(mx, my) else max(30, self.retry_text_pos[0]-2)

        self.back_text_pos[0] = min(50, self.back_text_pos[0]+2) if self.back_text_rect.collidepoint(mx, my) else max(30, self.back_text_pos[0]-2)

        display.blit(self.died_text, ((DISPLAY_WIDTH//2) - (self.died_text.get_rect().w//2), 50))
        display.blit(self.retry_text_surf, (self.retry_text_pos[0], self.retry_text_pos[1]))
        display.blit(self.back_text_surf, (self.back_text_pos[0], self.back_text_pos[1]))

    def render(self, scroll):
        display.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

    def shoot_bullet(self, scroll, player_bullet_group, dt):
        self.shooting_cd = max(.3, self.fire_rate / 1000)

        self.current_time += dt
        if self.is_shooting:

            if self.current_time - self.shoot_previous_time > self.shooting_cd:
                SFX.player_bullet_fire_sfx.play()

                mouse_x = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH) + scroll[0]
                mouse_y = (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT) + scroll[1]
                
                spread = 0
                if self.bullet_number >= 2:
                    spread = -10
                for i in range(self.bullet_number):
                    if self.bullet_number == 2 and i == 1:
                        spread = -spread
                    elif self.bullet_number == 3 and i >= 1:
                        spread += 10

                    bullet = PlayerBullet(self.rect.centerx, 
                                    self.rect.centery,
                                    self.bullet_speed,
                                    self.bullet_pierce_number,
                                    self.bullet_bounce_number, 
                                    self.x_direction,
                                    self.bullet_size_doubled_activated, 
                                    mouse_x,
                                    mouse_y,
                                    spread=spread)
                    player_bullet_group.add(bullet)
                    self.shoot_previous_time = self.current_time

    def player_is_hit(self, dt):
        self.is_hit_current_timer += dt

        if self.is_invincible:
            if self.is_hit_current_timer - self.invincible_timer > self.invincible_duration:
                self.is_invincible = False

            self.blink_timer += dt
            if self.blink_timer >= .1:
                self.blink_timer = 0
                self.blink_state = not self.blink_state
            
            if self.blink_state:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def create_dash_particles(self):
        # if len(self.dash_particles) < 10:
        for i in range(3):
            # loc, velocity, radius, dash direction, color
            angle = math.pi * random.uniform(.77, 1.3) if self.dash_direction > 0 else 2 * math.pi * random.uniform(.77, 1.3)
            speed = random.randint(1, 3)
            self.dash_particles.append([list(self.rect.center),
                                        [math.cos(angle)* speed, math.sin(angle)* speed],
                                        random.randint(8, 12),
                                        self.dash_direction,
                                        pygame.Color(random.randrange(204, 251), 255, 0)])
    
    def draw_dash_particles(self, scroll):
        if self.dash_particles:
            self.dash_particles = [p for p in self.dash_particles if p[2] > 0]

            for particle in self.dash_particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]

                particle[2] -= .3

                pygame.draw.circle(display, (60, 74, 0), (particle[0][0]-scroll[0]+4, particle[0][1]-scroll[1]+4), (particle[2]))
                pygame.draw.circle(display, particle[4], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), particle[2])

    def draw_glow(self, dark_overlay, scroll):
        # pygame.draw.rect(display,(255,0,0),(self.rect.x-scroll[0],self.rect.y-scroll[1],self.rect.w,self.rect.h),2)
        dark_overlay.blit(self.gradient_image,
                                (self.rect.x - scroll[0] - ((self.rect.w*2) + 32),
                                self.rect.y - scroll[1] - (self.rect.h*2)),
                                special_flags=pygame.BLEND_RGBA_ADD)
        
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
        player_tile_loc = (int(self.rect.midleft[0] // TILE_SIZE), int(self.rect.y // TILE_SIZE)+2)

        ground_offset_tiles = [(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1)]

        for offset in ground_offset_tiles:
            check_loc = str(player_tile_loc[0] + offset[0]) + ";" + str(player_tile_loc[1])
            if check_loc in tiles_blocks:
                if self.x_velocity != 0 and self.walk_timer == 0:
                    self.walk_timer = 45
                    random.choice(SFX.walk_sfx_list).play()
                self.on_ground = True

    def _move(self, keys_hold, jump_particles):
        if keys_hold[pygame.K_SPACE] and not self.jumping and self.on_ground:
            self.y_velocity = -1170 # ORIGINAL 1050
            self.jumping = True
            SFX.jump_sfx.play()
            for _ in range(3): # location, y_velocity, radius
                jump_particles.append([[random.randrange(self.rect.midbottom[0]-5, self.rect.midbottom[0]+5), self.rect.midbottom[1]],
                                       [random.randrange(-2, 2), 2],
                                       random.randrange(5, 8)]) 

        if not self.dash_num:
            if keys_hold[pygame.K_LSHIFT]:
                SFX.dash_sfx.play()
                self.dash_num = 60 if self.x_direction > 0 else -60
                self.dash_direction = 1 if self.x_direction > 0 else -1
                self.is_invincible = True
        if keys_hold[pygame.K_d]:
            self.x_velocity = self.movement_speed
            self.x_direction = 1
        if keys_hold[pygame.K_a]:
            self.x_velocity = -self.movement_speed
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
                    self.pos.x = tile.rect.left - PLAYER_WIDTH
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
                    self.pos.y = tile.rect.top - PLAYER_HEIGHT
                    self.rect.y = int(self.pos.y)
                    self.jumping = False
                elif self.y_velocity < 0:
                    self.pos.y = tile.rect.bottom
                    self.rect.y = int(self.pos.y)
                self.y_velocity = 0