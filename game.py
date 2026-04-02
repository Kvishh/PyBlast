import pygame, random, time, sys

import effects_sytem as fx
import collision_system as cs
import roll_system as rs
import spawn_system as ss
import pause as p
from state import State
from spawn_system import Enemies as ems
from configs import *
from images import CrosshairImage
from game_map import tiles_group, draw_background, create_tiles, draw_tiles, draw_behind_long_rocks, draw_front_long_rocks
from player import Player
from wand import Wand
from customgroup import CustomGroup
from hud import HUD
from light import Light
from shoot import Shoot
from burst import Burst
from specter import Specter

class Gameplay(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        # Setting custom cursor-----------------------------------------------------------------------------------
        crosshair_image = CrosshairImage.crosshair_image_scaled
        cursor = pygame.cursors.Cursor((16, 16,), crosshair_image)
        pygame.mouse.set_cursor(cursor)

        # GAME COMPONENTS-----------------------------------------------------------------------------------------
        # Scrolling (Camera effect)-------------------------------------------------------------------------------
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]

        ### INDIVIDUAL GROUPS ------------------------------------------------------------------------------------------------ ###
        # Player Group---------------------------------------------------------------------------------------------
        self.player_group = CustomGroup()

        # Player Bullet group--------------------------------------------------------------------------------------
        self.player_bullet_group = CustomGroup()


        ### INDIVIDUAL COMPONENTS --------------------------------------------------------------------------------------------- ###
        # Shake timer----------------------------------------------------------------------------------------------
        self.shake_timer = [0]

        # Player---------------------------------------------------------------------------------------------------
        self.player = Player((WINDOW_WIDTH // 2) - PLAYER_WIDTH, 365, self.player_group)

        # Wand-----------------------------------------------------------------------------------------------------
        self.wand = Wand(self.player.rect.centerx, self.player.rect.centery)

        # Light Enemy----------------------------------------------------------------------------------------------
        # self.light = Light(WINDOW_WIDTH-LIGHT_ENEMY_WIDTH, 0, ems.light_enemy_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, ems.all_ground_enemies, ems.all_enemies_group)
        # self.another_light = Light(300, 0, ems.light_enemy_group, ems.all_ground_enemies)
        # self.ground_en = Light(600, 0, ems.light_enemy_group, ems.all_ground_enemies)

        # Heavy Enemy----------------------------------------------------------------------------------------------
        # self.tank = Tank(WINDOW_WIDTH-HEAVY_ENEMY_WIDTH, FLOOR, ems.tank_enemy_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, ems.all_ground_enemies)

        # # Flight Enemy---------------------------------------------------------------------------------------------
        # self.flight_enemy = Flight(50, 0, ems.flight_enemy_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, ems.all_flying_enemies)

        # Soar Enemy-----------------------------------------------------------------------------------------------
        # self.soar_enemy = Soar(50, 0, ems.soar_enemy_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, ems.all_flying_enemies)

        # # Shooting Enemy-------------------------------------------------------------------------------------------
        # self.shoot_enemy = Shoot(250, 0, ems.shoot_enemy_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, ems.all_flying_enemies)

        # # Burst Shooting Enemy-------------------------------------------------------------------------------------
        # self.burst_enemy = Burst(350, 0, ems.burst_enemy_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, ems.all_flying_enemies)

        # # Specter Shooting Enemy-----------------------------------------------------------------------------------
        # self.specter_enemy = Specter(350, 0, ems.specter_enemy_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, ems.all_flying_enemies)


        ### FUNCTIONS BEFORE STARTING GAME LOOP ------------------------------------------------------------------------------ ###
        # Function for creating tile-------------------------------------------------------------------------------
        # This checks if tiles_group.sprites() is empty, if it is empty call the function
        if not tiles_group.sprites(): create_tiles()


        ### AGGREGATED GROUPS ------------------------------------------------------------------------------------------------ ###
        # Group for all projectiles that can hit tiles--------------------------------------------------------------
        self.all_projectile_that_hit_tiles = pygame.sprite.Group(*self.player_bullet_group, *ems.enemy_bullet_group)

        # Group for all projectiles that can hit player--------------------------------------------------------------
        self.all_enemy_projectiles_that_hit_player = pygame.sprite.Group(*ems.enemy_bullet_group, *ems.specter_enemy_bullet_group)


        ### Overlay and HUD -------------------------------------------------------------------------------------------------- ###
        # For HUD --------------------------------------------------------------------------------------------------
        self.hud = HUD(self.player)

        # Black Overlay -------------------------------------------------------------------------------------------
        self.dark_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.dark_overlay.fill((190,190,190,100))

        # Xp increment for level ----------------------------------------------------------------------------------
        self.xp_increment = [0]

        # Object responsible for pausing the game loop if in leveling up-------------------------------------------
        self.level_up_state = [False]


        # Spawning enemies --------------------------------------------------------------------------------------------------- ###
        # Spawn rect for ground enemies----------------------------------------------------------------------------
        self.spawn_rect = pygame.Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        # Set of enemies killed -----------------------------------------------------------------------------------
        self.enemies_killed = set([])

        # Set of current enemies present --------------------------------------------------------------------------
        self.set_of_alive_enemies = set([])

        # Current spawn session -----------------------------------------------------------------------------------
        self.spawn_session_num = 1

        # Spawn session timer -------------------------------------------------------------------------------------
        self.spawn_session_timer = 0


    def update(self):
        pause_screen = None
        last_frame = []

        pause_overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        pause_overlay.fill((0,0,0, 128))

        countdown_time = 600
        countdown_timer = 0
        countdown_time_text = time.strftime("%M:%S", time.gmtime(countdown_time))

        spawn_timer = 0

        
        timer_active = False
        dt_multiplier = 1
        
        death_start_time = 0
        death_slow_down = False

        win_start_time = 0
        win_slow_down = False

        retry = False

        running = True
        is_paused = [False]
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.is_shooting = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.is_shooting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Player can only pause when they are alive, else
                        # they can't pause
                        if self.player.alive() and not self.player.has_survived:
                            pause_screen = display.copy()
                            is_paused[0] = not is_paused[0]
                    if event.key == pygame.K_u:
                        self.hud.current_xp_width += 490
                        self.hud.update_level_bar(self.xp_increment, self.level_up_state, last_frame)

            enemy_shoot_sfx_count = [0]
            
            if not is_paused[0] and not self.level_up_state[0]:
                dt = clock.tick(FPS) / 1000
                display.fill((42, 59, 95))
                self.dark_overlay.fill((190,190,190,100))

                countdown_timer += dt
                spawn_timer += dt
                self.spawn_session_timer += dt

                # Countdown decrements 1 second if 1 second has passed
                # and if player is still alive and if player hasn't won
                # yet, if player is dead stop the countdown timer
                if countdown_timer >= 1 and self.player.alive() and not self.player.has_survived:
                    countdown_time -= 1
                    countdown_time_text = time.strftime("%M:%S", time.gmtime(countdown_time))
                    countdown_timer -= 1
                
                # Check if countdown time has reached 00:00
                if countdown_time <= 0:
                    self.player.has_survived = True
                
                if self.spawn_session_timer >= 60:
                    self.spawn_session_num = min(7, self.spawn_session_num + 1)
                    self.spawn_session_timer -= 60

                # Checks if enemies' projectiles are near player radius only
                # if player has obtained the ability to slow down movement
                if self.player.slow_time_active:
                    dt = cs.slow_down_time(self.player, self.all_enemy_projectiles_that_hit_player, dt)
                
                # If player has died, slow down time
                if death_slow_down or win_slow_down:
                    dt_multiplier = max(0.25, dt_multiplier - .1)
                    dt = max(0.0038, dt * dt_multiplier)

                # Changing the scroll (camera) value
                self.true_scroll[0] += (self.player.rect.x - self.true_scroll[0] - (DISPLAY_WIDTH//2 - PLAYER_WIDTH//2))/20
                self.true_scroll[1] += (self.player.rect.y - self.true_scroll[1] - (DISPLAY_HEIGHT//2 - PLAYER_HEIGHT//2))/20

                if self.true_scroll[0] < 0:
                    self.true_scroll[0] = 0
                elif self.true_scroll[0] > 1300-DISPLAY_WIDTH:
                    self.true_scroll[0] = 1300-DISPLAY_WIDTH 

                if self.true_scroll[1] < 0:
                    self.true_scroll[1] = 0
                elif self.true_scroll[1] > 800-DISPLAY_HEIGHT:
                    self.true_scroll[1] = 800-DISPLAY_HEIGHT

                # Actual values used in scrolling (camera)
                self.scroll = self.true_scroll.copy()
                self.scroll[0] = int(self.true_scroll[0])
                self.scroll[1] = int(self.true_scroll[1])

                # Movement of spawn rect x and y and limits
                self.spawn_rect.x = self.player.rect.centerx - DISPLAY_WIDTH // 2
                self.spawn_rect.y = self.player.rect.centery - DISPLAY_HEIGHT // 2
                if self.spawn_rect.x < 0:
                    self.spawn_rect.x = 0
                elif self.spawn_rect.x > 1300-DISPLAY_WIDTH:
                    self.spawn_rect.x = 1300-DISPLAY_WIDTH 

                if self.spawn_rect.y < 0:
                    self.spawn_rect.y = 0
                elif self.spawn_rect.y > 800-DISPLAY_HEIGHT:
                    self.spawn_rect.y = 800-DISPLAY_HEIGHT

                # Applying shake in scroll
                if self.shake_timer[0]:
                    self.scroll[0] += random.randint(-4, 4)
                    self.scroll[1] += random.randint(-4, 4)

                # Every 5 seconds spawn enemies
                if spawn_timer > 5:
                    ss.spawn_enemies(self.hud.level, self.spawn_rect, self.spawn_session_num, self.set_of_alive_enemies, countdown_time)
                    spawn_timer -= 5

                # For drawing background
                draw_background(self.scroll)

                # Drawing behind platforms but in front of background
                draw_behind_long_rocks(self.scroll)

                # For drawing tiles
                draw_tiles(self.scroll, countdown_time, dt)

                # Creating background particles
                fx.create_background_particles()
                
                # Drawing explosion impacts/sparks
                fx.draw_explosion_impact(self.scroll)

                # Drawing explosions
                fx.draw_explosions(self.scroll)

                # Drawing explosions
                fx.draw_explosion_radiations(self.scroll)

                # Drawing of player bullets
                self.player_bullet_group.update(dt, self.scroll, self.shake_timer)
                self.player_bullet_group.draw(display, self.scroll)

                # Update and draw methods of enemy bullet groups
                ems.enemy_bullet_group.update(dt, self.scroll)
                ems.enemy_bullet_group.draw(display, self.scroll)

                # Update and draw methods of specter enemy bullet groups
                ems.specter_enemy_bullet_group.update(dt, self.scroll)
                ems.specter_enemy_bullet_group.draw(display, self.scroll)

                # Check if enemies' projectiles hit player's negator
                if self.player.negator_active:
                    cs.projectiles_hit_negator(self.player, self.all_enemy_projectiles_that_hit_player)

                # Check if projectiles hit tiles
                cs.projectiles_hit_tiles(self.all_projectile_that_hit_tiles, self.shake_timer)

                # Check if projectiles hit player
                cs.projectiles_hit_player(self.player, self.wand, self.all_enemy_projectiles_that_hit_player, self.shake_timer, dt)

                # Check if player has been hit/touched by enemies
                cs.all_enemies_touch_player(self.player, self.wand, ems.all_enemies_group, dt)

                # Check if player bulllets hit every kind of enemies
                if self.player.bullets_explode_state:
                    cs.check_enemies_within_explosion_radius(self.player, self.hud, self.xp_increment, self.enemies_killed, self.player_bullet_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, self.shake_timer)
                else:
                    cs.player_bullet_hit_all_enemies(self.player, self.hud, self.xp_increment, self.enemies_killed, self.player_bullet_group, ems.all_enemies_that_can_be_hit_by_playerbullet_group, self.shake_timer)

                # Check if player bullet hit any flying enemies
                cs.player_bullet_hit_flying_enemies(self.player_bullet_group)

                # Check if player bullet hit any ground enemies
                cs.player_bullet_hit_ground_enemies(self.player_bullet_group)

                # Killing of enemies
                for enemy in self.enemies_killed: enemy.kill()

                # After killing enemies, remove them in current enemies on game
                for enemy in self.enemies_killed: self.set_of_alive_enemies.remove(enemy)

                if self.player.alive():
                    # Player and Wand update and draw methods
                    self.wand.update(self.player, self.scroll, self.player.rect.centerx, self.player.rect.centery, dt)
                    self.wand.render(self.scroll)
                    self.player.update(pygame.key.get_pressed(), dt, self.dark_overlay, self.scroll, self.wand, jump_particles=fx.FxList.jump_particles, player_bullet_group=self.player_bullet_group)
                    self.player.render(self.scroll)

                # Draw jump particles
                fx.draw_jump_particles(self.scroll)

                # Enemy update and render
                ems.light_enemy_group.update(dt, self.player, self.scroll, self.set_of_alive_enemies)
                ems.light_enemy_group.draw(display, self.scroll)

                # Heavy Enemy update and render
                ems.tank_enemy_group.update(dt, self.player, self.scroll, self.set_of_alive_enemies)
                ems.tank_enemy_group.draw(display, self.scroll)

                # Avoid overlapping between ground enemies
                cs.avoid_overlap(ems.all_ground_enemies)

                # Flight Enemy update and render
                ems.flight_enemy_group.update(self.player, dt, ems.all_flying_enemies, self.scroll)
                ems.flight_enemy_group.draw(display, self.scroll)

                # Soar Enemy update and render
                ems.soar_enemy_group.update(self.player, dt, ems.all_flying_enemies, self.scroll)
                ems.soar_enemy_group.draw(display, self.scroll)

                # Shooting Enemy update and render
                ems.shoot_enemy_group.update(ems.enemy_bullet_group, self.all_projectile_that_hit_tiles, self.all_enemy_projectiles_that_hit_player, self.player, dt, ems.all_flying_enemies, self.scroll, enemy_shoot_sfx_count)
                ems.shoot_enemy_group.draw(display, self.scroll)

                # Burst Enemy update and render
                ems.burst_enemy_group.update(ems.enemy_bullet_group, self.all_projectile_that_hit_tiles, self.all_enemy_projectiles_that_hit_player, self.player, dt, ems.all_flying_enemies, self.scroll, enemy_shoot_sfx_count)
                ems.burst_enemy_group.draw(display, self.scroll)

                # Specter Enemy update and render
                ems.specter_enemy_group.update(ems.specter_enemy_bullet_group, self.player, dt, ems.all_flying_enemies, self.all_enemy_projectiles_that_hit_player, enemy_shoot_sfx_count)
                ems.specter_enemy_group.draw(display, self.scroll)

                # Drawing impacts/sparks
                fx.draw_impact(self.scroll)

                # Drawing particles
                fx.draw_floating_particles(self.scroll)

                # Drawing falling particles
                fx.draw_falling_particles(self.scroll)

                # Drawing radiation
                fx.draw_radiations(self.scroll)

                # Drawing debris
                fx.draw_debris(self.scroll)

                # Drawing background particles
                fx.draw_background_particles(self.dark_overlay, self.scroll, dt)
                display.blit(self.dark_overlay, (0,0), special_flags=pygame.BLEND_RGB_MULT)

                # Rendering of front objects (long rocks)
                draw_front_long_rocks(self.scroll)

                # Shake timer decrement
                if self.shake_timer[0] > 0:
                    self.shake_timer[0] -= 1
                
                if self.player.hurt_overlay_alpha:
                    self.player.hurt_overlay.fill((255,0,0,self.player.hurt_overlay_alpha))
                    display.blit(self.player.hurt_overlay, (0,0))

                    self.player.hurt_overlay_alpha = max(0, self.player.hurt_overlay_alpha-1)
                
                # HUD update
                # self.hud.update(countdown_time_text, self.xp_increment, self.level_up_state, last_frame)
                # The split is done to separate the minute (00) and seconds (59) since they are used as keys for cache
                self.hud.update(self.player, countdown_time_text.split(":"), self.xp_increment, self.level_up_state, last_frame)

                # If player is killed 
                if not self.player.alive():
                    display.blit(pause_overlay, (0,0))
                    death_slow_down = True

                    if not timer_active:
                        death_start_time = pygame.time.get_ticks()
                        timer_active = True

                    if timer_active:
                        current_time = pygame.time.get_ticks()
                        # Check if 1 seconds has passed since player died
                        if current_time - death_start_time >= 1000:
                            self.player.show_after_death_options(events)
                
                # If player won/survived
                if self.player.has_survived:
                    display.blit(pause_overlay, (0,0))
                    win_slow_down = True

                    if not timer_active:
                        win_start_time = pygame.time.get_ticks()
                        timer_active = True

                    if timer_active:
                        current_time = pygame.time.get_ticks()
                        # Check if 1 seconds has passed since player won
                        if current_time - win_start_time >= 1000:
                            self.player.show_after_winning_options(events)

                # Clearing of set
                self.enemies_killed.clear()

                # Reset for xp_increment so that when it levels up it does not add the old values
                # It will not accumulate. It is not cumulative
                self.xp_increment[0] = 0
            elif is_paused[0]:
                # Blitting of the last screen and the dark overlay when paused
                display.blit(pause_screen, (0,0))
                display.blit((pause_overlay), (0,0))

                exit = p.show_pause_options(events, is_paused)

                if exit is not None:
                    if exit == True: break

                    if exit == False:
                        retry = True
                        break

                clock.tick()
                self.player.is_shooting = False
            elif self.level_up_state[0]:
                display.blit(last_frame[0], (0,0))
                display.blit((pause_overlay), (0,0))

                rs.roll(events, self.level_up_state, self.player, last_frame)

                clock.tick()
                self.player.is_shooting = False

            # last methods to be called
            window.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
            pygame.display.flip()
        
        self.state_manager.state_stack.pop()

        # Reset, this happens so that the old status/upgrades done in last game
        # wouldn't get pass to another game if player retried the game
        self.reset_game()

        if retry: return "retry"
    
    def reset_game(self):
        for group in ss.Enemies.list_of_all_groups:
            group.empty()
        
        for tree in rs.RollSystem.list_of_skill_trees:
            for skill in tree.abilities_list:
                skill.acquired = False
            tree.is_exhausted = False

        fx.FxList.sparks.clear()
        fx.FxList.explosion_sparks.clear()
        fx.FxList.explosions.clear()
        fx.FxList.explosion_radiations.clear()
        fx.FxList.particles.clear()
        fx.FxList.falling_particles.clear()
        fx.FxList.radiations.clear()
        fx.FxList.debris.clear()
        fx.FxList.jump_particles.clear()