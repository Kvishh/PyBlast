import pygame, random, math
from configs import *
from game_map import tiles_group, tiles_blocks, draw_background, create_tiles, load_bg_images, load_long_rocks, draw_tiles, draw_behind_long_rocks, draw_front_long_rocks
from player import Player
from wand import Wand
from bullet import PlayerBullet
from customgroup import CustomGroup
from enemy import Light
from spark import Spark
from flying_enemy import FlyingEnemy
from shooting_enemy import ShootingEnemy
from tank import Tank


class Game:
    def __init__(self):
        # Initialize pygame---------------------------------------------------------------------------------------
        pygame.init()

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

        # Flying enemy group---------------------------------------------------------------------------------------
        self.flying_enemy_group = CustomGroup()

        # Shooting enemy group-------------------------------------------------------------------------------------
        self.shooting_enemy_group = CustomGroup()

        # Player Bullet group--------------------------------------------------------------------------------------
        self.player_bullet_group = CustomGroup()

        # Enemy Bullet group---------------------------------------------------------------------------------------
        self.enemy_bullet_group = CustomGroup()


        ### RELATED GROUPS --------------------------------------------------------------------------------------------------- ###
        # For walking enemies--------------------------------------------------------------------------------------
        self.all_ground_enemies = CustomGroup(self.light_enemy_group, self.tank_enemy_group)

        # For flying enemies---------------------------------------------------------------------------------------
        self.all_flying_enemies = CustomGroup(self.flying_enemy_group, self.shooting_enemy_group)


        ### INDIVIDUAL COMPONENTS --------------------------------------------------------------------------------------------- ###
        # Shake timer----------------------------------------------------------------------------------------------
        self.shake_timer = 0

        # Player---------------------------------------------------------------------------------------------------
        self.player = Player(WINDOW_WIDTH - PLAYER_WIDTH, 0)

        # Wand-----------------------------------------------------------------------------------------------------
        self.wand = Wand(self.player.rect.centerx, self.player.rect.centery)

        # Light Enemy----------------------------------------------------------------------------------------------
        self.light = Light(0, 0, self.light_enemy_group, self.all_ground_enemies)
        self.another_light = Light(300, 0, self.light_enemy_group, self.all_ground_enemies)
        self.ground_en = Light(600, 0, self.light_enemy_group, self.all_ground_enemies)

        # Heavy Enemy----------------------------------------------------------------------------------------------
        self.tank = Tank(WINDOW_WIDTH-HEAVY_ENEMY_WIDTH, 0, self.tank_enemy_group, self.all_ground_enemies)

        # Flying Enemy---------------------------------------------------------------------------------------------
        self.flying_enemy = FlyingEnemy(50, 0, self.flying_enemy_group, self.all_flying_enemies)

        # Shooting Enemy-------------------------------------------------------------------------------------------
        self.shooting_enemy = ShootingEnemy(250, 0, self.shooting_enemy_group, self.all_flying_enemies)


        ### EFFECTS LIST ---------------------------------------------------------------------------------------------------- ###
        # For background particles---------------------------------------------------------------------------------
        self.background_particles = []

        # For sparks-----------------------------------------------------------------------------------------------
        self.sparks = []

        # For particles--------------------------------------------------------------------------------------------
        self.particles = []

        # For falling particles------------------------------------------------------------------------------------
        self.falling_particles = []

        # For radiation--------------------------------------------------------------------------------------------
        self.radiations = []

        # For debris-----------------------------------------------------------------------------------------------
        self.debris = []


        ### FUNCTIONS BEFORE STARTING GAME LOOP ------------------------------------------------------------------------------- ###
        # Function for creating tile-------------------------------------------------------------------------------
        create_tiles()

        # Function for creating background-------------------------------------------------------------------------
        load_bg_images()

        # Function for loading background images-------------------------------------------------------------------
        load_long_rocks()


        ### AGGREGATED GROUPS ------------------------------------------------------------------------------------------------ ###
        # For every sprite when collided with bullet it will create spark------------------------------------------
        self.all_sprites_group = pygame.sprite.Group(tiles_group, self.all_ground_enemies, self.flying_enemy_group, self.shooting_enemy_group)

        # For shooting enemy when enemy bullet hits player and tiles-----------------------------------------------
        self.enemy_hits = pygame.sprite.Group(tiles_group, self.player_group)

        # Group for all projectiles---------------------------------------------------------------------------------
        self.all_bullets_group = CustomGroup(self.player_bullet_group, self.enemy_bullet_group)


    def game_run(self):
        previous_time = [pygame.time.get_ticks()]
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dt = clock.tick(FPS) / 1000
            display.fill((42, 59, 95))

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

            # Applying shake in scroll
            if self.shake_timer:
                self.scroll[0] += random.randint(-4, 4)
                self.scroll[1] += random.randint(-4, 4)

            # For drawing background
            draw_background(self.scroll)

            # Drawing behind platforms but in front of background
            draw_behind_long_rocks(self.scroll)

            # For drawing tiles
            draw_tiles(self.scroll)

            # Creating background particles
            self.create_background_particles()

            # Checking of mouse hold and creation of bullet
            self.shoot_bullet(previous_time, self.player.rect.centerx, self.player.rect.centery)

            # Drawing of player bullets
            self.player_bullet_group.update(dt, self.scroll)
            self.player_bullet_group.draw(display, self.scroll)

            # Update and draw methods of enemy bullet groups
            self.enemy_bullet_group.update(dt, self.scroll)
            self.enemy_bullet_group.draw(display, self.scroll)

            # Create debris
            self.create_debris()

            # Enemy bullet hit player
            self.enemy_bullets_hit_player()

            # Creating and drawing sparks
            self.create_impact_and_floating_particles()
            self.draw_impact()

            # Creating falling particles
            self.create_falling_particles()

            # Create radiations
            self.create_radiation()

            # Player and Wand update and draw methods
            self.wand.update(self.player, self.scroll, self.player.rect.centerx, self.player.rect.centery)
            self.wand.render(self.scroll)
            self.player.update(pygame.key.get_pressed(), dt)
            self.player.render(self.scroll)

            # Enemy update and render
            self.light_enemy_group.update(dt, self.player)
            self.light_enemy_group.draw(display, self.scroll)

            # # Avoid overlapping between ground enemies
            self.avoid_overlap()

            # # Heave Enemy update and render
            self.tank_enemy_group.update(dt, self.player)
            self.tank_enemy_group.draw(display, self.scroll)

            # # Flying Enemy update and render
            self.flying_enemy_group.update(self.player, dt, self.all_flying_enemies)
            self.flying_enemy_group.draw(display, self.scroll)

            # # # Shooting Enemy update and render
            self.shooting_enemy_group.update(self.enemy_bullet_group, self.all_bullets_group, self.player, dt, self.all_flying_enemies)
            self.shooting_enemy_group.draw(display, self.scroll)

            # Drawing particles
            self.draw_floating_particles()

            # Drawing falling particles
            self.draw_falling_particles()

            # Drawing radiation
            self.draw_radiations()

            # Drawing debris
            self.draw_debris()

            # Rendering of front objects (long rocks)
            draw_front_long_rocks(self.scroll)

            # Drawing background particles
            self.draw_background_particles()

            # Shake timer decrement
            if self.shake_timer > 0:
                self.shake_timer -= 1

            # last methods to be called
            window.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
            pygame.display.flip()
        
        # Quit the window
        pygame.quit()

    def avoid_overlap(self):
        for x in self.all_ground_enemies:
            for y in self.all_ground_enemies:
                if x is y:
                    continue

                if x.rect.colliderect(y.rect):
                    overlap = x.rect.clip(y.rect)

                    if overlap.w < overlap.h:
                        if x.rect.centerx < y.rect.centerx:
                            x.pos.x -= overlap.w // 6
                            y.pos.x += overlap.w // 6
                        else:
                            x.pos.x += overlap.w // 6
                            y.pos.x -= overlap.w // 6
                    elif overlap.h < overlap.w:
                            x.pos.x += overlap.h // 6
                            y.pos.x -= overlap.h // 6

    def shoot_bullet(self, previous_time, player_rect_centerx, player_rect_centery):
        mouse_hold = pygame.mouse.get_pressed()
        if mouse_hold[0]:
            current_time = pygame.time.get_ticks()
            if current_time - previous_time[0] > SHOOTING_COOLDOWN:

                mouse_x = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH) + self.scroll[0]
                mouse_y = (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT) + self.scroll[1]
                
                bullet = PlayerBullet("assets/images/bullet.png", 
                                player_rect_centerx, 
                                player_rect_centery, 
                                self.player.x_direction, 
                                mouse_x,
                                mouse_y)
                self.player_bullet_group.add(bullet)
                self.all_bullets_group.add(bullet)
                previous_time[0] = current_time

    def create_background_particles(self):
        if len(self.background_particles) < 7: # loc, radius, direction
            self.background_particles.append([[random.randrange(WINDOW_WIDTH), random.randrange(WINDOW_HEIGHT)],
                                        random.randrange(2, 4),
                                        [random.choice([.5, -.5]), random.choice([.5, -.5])]])

    def draw_background_particles(self):
        if self.background_particles:
            self.background_particles = [background_particle for background_particle in self.background_particles
                                    if (background_particle[0][1] > 0 and background_particle[0][1] < WINDOW_HEIGHT) and 
                                    (background_particle[0][0] > 0 and background_particle[0][0] < WINDOW_WIDTH)]            
            
            # loc, radius, direction
            for bg_particle in self.background_particles:
                # bg_particle[0][1] += -.5
                bg_particle[0][0] += bg_particle[2][0]
                bg_particle[0][1] += bg_particle[2][1]
                pygame.draw.circle(display, (255, 255, 255), [int(bg_particle[0][0])-self.scroll[0], int(bg_particle[0][1])-self.scroll[1]], bg_particle[1])

                # change the multiplier if you want to make the glow particle (circle) to be bigger
                bg_particle_radius = bg_particle[1]*3

                particle_surface = pygame.Surface((bg_particle_radius * 2, bg_particle_radius * 2))
                pygame.draw.circle(particle_surface, (20, 20, 20), (bg_particle_radius, bg_particle_radius), bg_particle_radius)
                # pygame.draw.circle(particle_surface, (20, 20, 20), (bg_particle_radius-scroll[0], bg_particle_radius-scroll[1]), bg_particle_radius) # ORIGINAL!!
                particle_surface.set_colorkey((0,0,0))

                display.blit(particle_surface, [int(bg_particle[0][0] - bg_particle_radius)-self.scroll[0], int(bg_particle[0][1] - bg_particle_radius)-self.scroll[1]], special_flags=pygame.BLEND_RGB_ADD)

    def create_impact_and_floating_particles(self):
        hits = pygame.sprite.groupcollide(self.player_bullet_group, self.all_sprites_group, False, False)

        for bullet, collided_sprites in hits.items():
            self.shake_timer = 20
            self.create_floating_particles(bullet.rect.center)

            for _ in range(6):
                self.sparks.append(Spark([bullet.rect.centerx, bullet.rect.centery], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))
    
    def enemy_bullets_hit_player(self):
        hits = pygame.sprite.groupcollide(self.enemy_bullet_group, self.enemy_hits, True, False)

        for bullet, sprite_collided in hits.items():
            self.shake_timer = 20
            self.create_floating_particles(bullet.rect.center)

            for _ in range(6):
                self.sparks.append(Spark([bullet.rect.centerx, bullet.rect.centery], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))            

    def draw_impact(self):
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.move(1)
            spark.draw(display, self.scroll)
            if not spark.alive:
                self.sparks.pop(i)

    def create_floating_particles(self, pos):
        pos = list(pos)
        for _ in range(15): # location, velocity, radius, color
            self.particles.append([[random.randrange(pos[0]-30, pos[0]+30), random.randrange(pos[1]-20, pos[1]+20)],
                                    [random.randrange(-3, 3), -3], 
                                    random.randrange(24, 30),
                                    255])
    
    def create_falling_particles(self):
        hits = pygame.sprite.groupcollide(self.player_bullet_group, self.all_ground_enemies, True, False)

        for bullet, enemies in hits.items():
            pos = list(bullet.rect.center)
            for enemy in enemies:
                if isinstance(enemy, Light):
                    for _ in range(20): # location, velocity, radius, color
                        self.falling_particles.append([[random.randrange(pos[0]-20, pos[0]+20), random.randrange(pos[1]-20, pos[1]+20)],
                                                [random.randrange(-3, 3), -2], 
                                                random.randrange(10, 14),
                                                (78, 45, 145)])
                elif isinstance(enemy, Tank):
                    for _ in range(20): # location, velocity, radius
                        self.falling_particles.append([[random.randrange(pos[0]-20, pos[0]+20), random.randrange(pos[1]-20, pos[1]+20)],
                                                [random.randrange(-3, 3), -2], 
                                                random.randrange(10, 14),
                                                (135, 152, 173)])

    def create_radiation(self):
        hits = pygame.sprite.groupcollide(self.player_bullet_group, self.all_flying_enemies, True, False)

        for bullet, enemy in hits.items():
            pos = list(bullet.rect.center)
            # location, radius, width
            self.radiations.append([[pos[0], pos[1]],
                                    15,
                                    8])

    def create_debris(self):
        hits = pygame.sprite.groupcollide(self.all_bullets_group, tiles_group, False, False)

        for bullet, tiles_hit_list in hits.items():
            pos = list(bullet.rect.center) # location, velocity, radius, color
            for _ in range(20):
                r = random.randrange(60, 80)
                g = r
                self.debris.append([[pos[0], pos[1]], # x axis random.randrange(pos[0]-20, pos[0]+20) ; y axis random.randrange(pos[1]-20, pos[1]+20)
                            [random.randrange(-3, 3), random.randrange(-3, 3)], 
                            random.randrange(10, 16),
                            (r, g, 125)])

    def draw_floating_particles(self):
        if self.particles:
            self.particles = [particle for particle in self.particles if particle[2] > 0]

            for particle in self.particles:
                # radius decrement
                particle[2] -= .4

                # change position over time
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]

                # change y velocity over time
                particle[1][1] += .02

                # change color over time
                particle[3] -= random.randint(1, 3)
                pygame.draw.circle(display,
                                   (int(particle[3]), int(particle[3]), int(particle[3])),
                                   (particle[0][0] - self.scroll[0], particle[0][1] - self.scroll[1]),
                                   int(particle[2]))

    def draw_falling_particles(self):
        if self.falling_particles:
            self.falling_particles = [particle for particle in self.falling_particles if particle[2] > 0]

            for particle in self.falling_particles:
                # radius decrement
                particle[2] -= .2

                # change position over time
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]

                # change y velocity over time
                particle[1][1] += .2

                pygame.draw.circle(display,
                                   (32, 33, 48),
                                   (particle[0][0] + 3 - self.scroll[0], particle[0][1] + 3 - self.scroll[1]),
                                   int(particle[2]))

                pygame.draw.circle(display,
                                   particle[3],
                                   (particle[0][0] - self.scroll[0], particle[0][1] - self.scroll[1]),
                                   int(particle[2]))

    def draw_radiations(self):
        if self.radiations:
            self.radiations = [radiation for radiation in self.radiations if radiation[2] > 1.1]

            for radiation in self.radiations:
                radiation[1] += 6 # radius
                radiation[2] -= .1 # width

                pygame.draw.circle(display,
                                   (35, 61, 37),
                                   (radiation[0][0] + 6 - self.scroll[0], radiation[0][1] + 3 - self.scroll[1]), int(radiation[1]),
                                   int(radiation[2]))

                pygame.draw.circle(display,
                                   (81, 143, 85),
                                   (radiation[0][0]-self.scroll[0], radiation[0][1]-self.scroll[1]), int(radiation[1]),
                                   int(radiation[2]))
    
    def draw_debris(self):
        if self.debris:
            self.debris = [debris for debris in self.debris if debris[2] > 0]

            for debris in self.debris:
                # radius decrement
                debris[2] -= .1

                # change position over time
                debris[0][0] += debris[1][0]
                debris_loc = str(int(debris[0][0] / TILE_SIZE)) + ';' + str(int(debris[0][1] / TILE_SIZE))
                if debris_loc in tiles_blocks:
                    debris[1][0] = -.85 * debris[1][0]
                    debris[1][1] *= 0.95
                    debris[0][0] += debris[1][0] * 2

                debris[0][1] += debris[1][1]
                debris_loc = str(int(debris[0][0] / TILE_SIZE)) + ';' + str(int(debris[0][1] / TILE_SIZE))
                if debris_loc in tiles_blocks:
                    debris[1][1] = -.65 * debris[1][1]
                    debris[1][0] *= 0.95
                    debris[0][1] += debris[1][1] * 2

                # change y velocity over time
                debris[1][1] += .2

                pygame.draw.circle(display,
                                   (32, 33, 48),
                                   (debris[0][0] + 5 - self.scroll[0], debris[0][1] + 5 - self.scroll[1]),
                                   debris[2])

                pygame.draw.circle(display,
                                   debris[3],
                                   (debris[0][0] - self.scroll[0], debris[0][1] - self.scroll[1]),
                                   debris[2])
