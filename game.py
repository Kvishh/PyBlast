import pygame, random, math, time
import effects_sytem as fx
import collision_system as cs
from configs import *
from game_map import tiles_blocks, draw_background, create_tiles, draw_tiles, draw_behind_long_rocks, draw_front_long_rocks
from player import Player
from wand import Wand
from customgroup import CustomGroup, ShootCustomGroup
from light import Light
from flight import Flight
from soar import Soar
from shoot import Shoot
from burst import Burst
from specter import Specter
from tank import Tank
from hud import HUD


class Game:
    def __init__(self):
        # Initialize pygame---------------------------------------------------------------------------------------
        pygame.init()

        # Setting custom cursor-----------------------------------------------------------------------------------
        crosshair_image = pygame.transform.scale(pygame.image.load("assets/images/crosshair.png").convert_alpha(), (32, 32))
        cursor = pygame.cursors.Cursor((16, 16,), crosshair_image)
        pygame.mouse.set_cursor(cursor)

        # GAME COMPONENTS-----------------------------------------------------------------------------------------
        # Scrolling (Camera effect)-------------------------------------------------------------------------------
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]

        ### INDIVIDUAL GROUPS ------------------------------------------------------------------------------------------------ ###
        # Player Group---------------------------------------------------------------------------------------------
        self.player_group = CustomGroup()

        # Light enemy Group----------------------------------------------------------------------------------------
        self.light_enemy_group = CustomGroup()

        # Tank enemy Group-----------------------------------------------------------------------------------------
        self.tank_enemy_group = CustomGroup()

        # Flight enemy group---------------------------------------------------------------------------------------
        self.flight_enemy_group = CustomGroup()

        # Soar enemy group-----------------------------------------------------------------------------------------
        self.soar_enemy_group = CustomGroup()        

        # Shooting enemy group-------------------------------------------------------------------------------------
        self.shoot_enemy_group = ShootCustomGroup()

        # Burst enemy group----------------------------------------------------------------------------------------
        self.burst_enemy_group = ShootCustomGroup()

        # Specter enemy group--------------------------------------------------------------------------------------
        self.specter_enemy_group = ShootCustomGroup()

        # Player Bullet group--------------------------------------------------------------------------------------
        self.player_bullet_group = CustomGroup()

        # Enemy Bullet group---------------------------------------------------------------------------------------
        self.enemy_bullet_group = CustomGroup()

        # Specter Enemy Bullet group-------------------------------------------------------------------------------
        self.specter_enemy_bullet_group = CustomGroup()


        ### RELATED GROUPS --------------------------------------------------------------------------------------------------- ###
        # For walking enemies--------------------------------------------------------------------------------------
        self.all_ground_enemies = CustomGroup(self.light_enemy_group, self.tank_enemy_group)

        # For flying enemies---------------------------------------------------------------------------------------
        self.all_flying_enemies = CustomGroup(self.flight_enemy_group, self.soar_enemy_group, self.shoot_enemy_group, self.burst_enemy_group, self.specter_enemy_group)


        ### INDIVIDUAL COMPONENTS --------------------------------------------------------------------------------------------- ###
        # Shake timer----------------------------------------------------------------------------------------------
        self.shake_timer = [0]

        # Player---------------------------------------------------------------------------------------------------
        self.player = Player(0, 0, self.player_group)

        # Wand-----------------------------------------------------------------------------------------------------
        self.wand = Wand(self.player.rect.centerx, self.player.rect.centery)

        # Light Enemy----------------------------------------------------------------------------------------------
        self.light = Light(0, 0, self.light_enemy_group, self.all_ground_enemies)
        self.another_light = Light(300, 0, self.light_enemy_group, self.all_ground_enemies)
        self.ground_en = Light(600, 0, self.light_enemy_group, self.all_ground_enemies)

        # Heavy Enemy----------------------------------------------------------------------------------------------
        self.tank = Tank(WINDOW_WIDTH-HEAVY_ENEMY_WIDTH, 0, self.tank_enemy_group, self.all_ground_enemies)

        # Flight Enemy---------------------------------------------------------------------------------------------
        self.flight_enemy = Flight(50, 0, self.flight_enemy_group, self.all_flying_enemies)

        # Soar Enemy-----------------------------------------------------------------------------------------------
        self.soar_enemy = Soar(50, 0, self.soar_enemy_group, self.all_flying_enemies)

        # Shooting Enemy-------------------------------------------------------------------------------------------
        self.shoot_enemy = Shoot(250, 0, self.shoot_enemy_group, self.all_flying_enemies)

        # Burst Shooting Enemy-------------------------------------------------------------------------------------
        self.burst_enemy = Burst(350, 0, self.burst_enemy_group, self.all_flying_enemies)

        # Specter Shooting Enemy-----------------------------------------------------------------------------------
        self.specter_enemy = Specter(350, 0, self.specter_enemy_group, self.all_flying_enemies)


        ### FUNCTIONS BEFORE STARTING GAME LOOP ------------------------------------------------------------------------------ ###
        # Function for creating tile-------------------------------------------------------------------------------
        create_tiles()


        ### AGGREGATED GROUPS ------------------------------------------------------------------------------------------------ ###
        # Group for of all enemies that can damage player-----------------------------------------------------------
        self.all_enemies_group = pygame.sprite.Group(*self.all_ground_enemies, *self.all_flying_enemies)

        # Group for all enemies that can be detected as hit by player bullet----------------------------------------
        self.all_enemies_that_can_be_hit_by_playerbullet_group = pygame.sprite.Group(*self.all_ground_enemies, *self.flight_enemy_group, *self.soar_enemy_group, *self.shoot_enemy_group, *self.burst_enemy_group, *self.specter_enemy_group)

        # Group for all projectiles that can hit tiles--------------------------------------------------------------
        self.all_projectile_that_hit_tiles = pygame.sprite.Group(*self.player_bullet_group, *self.enemy_bullet_group)

        # Group for all projectiles that can hit player--------------------------------------------------------------
        self.all_enemy_projectiles_that_hit_player = pygame.sprite.Group(*self.enemy_bullet_group, *self.specter_enemy_bullet_group)


        ### Overlay and HUD -------------------------------------------------------------------------------------------------- ###
        # For HUD --------------------------------------------------------------------------------------------------
        self.hud = HUD(self.player)

        # Black Overlay -------------------------------------------------------------------------------------------
        self.dark_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.dark_overlay.fill((190,190,190,100))

        # Xp increment for level ----------------------------------------------------------------------------------
        self.xp_increment = 0

        # Set of enemies killed -----------------------------------------------------------------------------------
        self.enemies_killed = set([])

        # Spawn rect for ground enemies-----------------------------------------------------------------------------
        self.spawn_rect = pygame.Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)


    def game_run(self):
        interval = [pygame.time.get_ticks()]

        pause_screen = None

        pause_overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        pause_overlay.fill((0,0,0, 128))

        countdown_time = 600
        countdown_time_text = time.strftime("%M:%S", time.gmtime(countdown_time))
        timer_evt = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_evt, 1000)


        running = True
        is_paused = False
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_screen = display.copy()
                        is_paused = not is_paused
                    if event.key == pygame.K_u:
                        self.hud.current_xp_width += 490
            
            if not is_paused:
                for event in events:
                    if event.type == timer_evt:
                        countdown_time -= 1
                        countdown_time_text = time.strftime("%M:%S", time.gmtime(countdown_time))

                dt = clock.tick(FPS) / 1000
                display.fill((42, 59, 95))
                self.dark_overlay.fill((190,190,190,100))

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

                # Spawn ground enemies 
                self.spawn_ground_enemies(interval)

                # For drawing background
                draw_background(self.scroll)

                # Drawing behind platforms but in front of background
                draw_behind_long_rocks(self.scroll)

                # For drawing tiles
                draw_tiles(self.scroll)

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
                self.enemy_bullet_group.update(dt, self.scroll)
                self.enemy_bullet_group.draw(display, self.scroll)

                # Update and draw methods of specter enemy bullet groups
                self.specter_enemy_bullet_group.update(dt, self.scroll)
                self.specter_enemy_bullet_group.draw(display, self.scroll)

                # Check if enemies' projectiles hit player's negator
                if self.player.negator_active:
                    cs.projectiles_hit_negator(self.player, self.all_enemy_projectiles_that_hit_player)

                # Check if projectiles hit tiles
                cs.projectiles_hit_tiles(self.all_projectile_that_hit_tiles, self.shake_timer)

                # Check if projectiles hit player
                cs.projectiles_hit_player(self.player, self.wand, self.all_enemy_projectiles_that_hit_player, self.shake_timer)

                # Check if player has been hit/touched by enemies
                cs.all_enemies_touch_player(self.player, self.wand, self.all_enemies_group)

                # Check if player bulllets hit every kind of enemies
                if self.player.bullets_explode_state:
                    cs.check_enemies_within_explosion_radius(self.player, self.hud, self.enemies_killed, self.player_bullet_group, self.all_enemies_that_can_be_hit_by_playerbullet_group, self.shake_timer)
                else:
                    cs.player_bullet_hit_all_enemies(self.player, self.hud, self.xp_increment, self.enemies_killed, self.player_bullet_group, self.all_enemies_that_can_be_hit_by_playerbullet_group, self.shake_timer)

                # Check if player bullet hit any flying enemies
                cs.player_bullet_hit_flying_enemies(self.player_bullet_group)

                # Check if player bullet hit any ground enemies
                cs.player_bullet_hit_ground_enemies(self.player_bullet_group)

                # Player and Wand update and draw methods
                self.wand.update(self.player, self.scroll, self.player.rect.centerx, self.player.rect.centery)
                self.wand.render(self.scroll)
                self.player.update(pygame.key.get_pressed(), dt, fx.FxList.jump_particles, self.dark_overlay, self.scroll, self.player_bullet_group)
                self.player.render(self.scroll)

                # Draw jump particles
                fx.draw_jump_particles(self.scroll)

                # # Enemy update and render
                # self.light_enemy_group.update(dt, self.player, self.scroll)
                # self.light_enemy_group.draw(display, self.scroll)

                # # Heavy Enemy update and render
                # self.tank_enemy_group.update(dt, self.player, self.scroll)
                # self.tank_enemy_group.draw(display, self.scroll)

                # # Avoid overlapping between ground enemies
                # cs.avoid_overlap(self.all_ground_enemies)

                # # Flight Enemy update and render
                # self.flight_enemy_group.update(self.player, dt, self.all_flying_enemies, self.scroll)
                # self.flight_enemy_group.draw(display, self.scroll)

                # # Soar Enemy update and render
                # self.soar_enemy_group.update(self.player, dt, self.all_flying_enemies, self.scroll)
                # self.soar_enemy_group.draw(display, self.scroll)

                # Shooting Enemy update and render
                self.shoot_enemy_group.update(self.enemy_bullet_group, self.all_projectile_that_hit_tiles, self.all_enemy_projectiles_that_hit_player, self.player, dt, self.all_flying_enemies, self.scroll)
                self.shoot_enemy_group.draw(display, self.scroll)

                # Burst Enemy update and render
                self.burst_enemy_group.update(self.enemy_bullet_group, self.all_projectile_that_hit_tiles, self.all_enemy_projectiles_that_hit_player, self.player, dt, self.all_flying_enemies, self.scroll)
                self.burst_enemy_group.draw(display, self.scroll)

                # Specter Enemy update and render
                self.specter_enemy_group.update(self.specter_enemy_bullet_group, self.player, dt, self.all_flying_enemies, self.all_enemy_projectiles_that_hit_player)
                self.specter_enemy_group.draw(display, self.scroll)

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
                fx.draw_background_particles(self.dark_overlay, self.scroll)
                display.blit(self.dark_overlay, (0,0), special_flags=pygame.BLEND_RGB_MULT)

                # Rendering of front objects (long rocks)
                draw_front_long_rocks(self.scroll)

                # Shake timer decrement
                if self.shake_timer[0] > 0:
                    self.shake_timer[0] -= 1

                # Increase of level width
                self.xp_increment *= len(self.enemies_killed)

                # Killing of enemies
                for enemy in self.enemies_killed: enemy.kill()
                
                # HUD update
                self.hud.update(countdown_time_text)

                ###############################################
                self.hud.update_level_bar(self.xp_increment)
                ###############################################

                # Reset of set and xp_increment
                self.enemies_killed.clear()
                self.xp_increment = 0
            elif is_paused:
                # Blitting of the last screen and the dark overlay when paused
                display.blit(pause_screen, (0,0))
                display.blit((pause_overlay), (0,0))
                clock.tick()

            # last methods to be called
            window.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
            pygame.display.flip()
        
        # Quit the window
        pygame.quit()

    def spawn_ground_enemies(self, interval):
        now = pygame.time.get_ticks()
        if now - interval[0] > 5000:
            interval[0] = now

            x = random.randint(0, WINDOW_WIDTH-HEAVY_ENEMY_WIDTH)
            while True:
                x = random.randint(0, WINDOW_WIDTH-HEAVY_ENEMY_WIDTH)
                if x < self.spawn_rect.left or x > self.spawn_rect.right:
                    break
            Tank(x, FLOOR, self.tank_enemy_group, self.all_ground_enemies, self.all_enemies_that_can_be_hit_by_playerbullet_group, self.all_enemies_group)