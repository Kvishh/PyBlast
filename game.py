import pygame, random, math
from configs import *
from game_map import tiles_group, draw_background, create_tiles, load_bg_images, load_long_rocks, draw_tiles, draw_behind_long_rocks, draw_front_long_rocks
from player import Player
from wand import Wand
from bullet import Bullet
from customgroup import CustomGroup
from enemy import Enemy
from spark import Spark
from flying_enemy import FlyingEnemy
from shooting_enemy import ShootingEnemy


class Game:
    def __init__(self):
        # Initialize pygame--------------------------------------------------------------
        pygame.init()

        # GAME COMPONENTS----------------------------------------------------------------
        # Scrolling (Camera effect)------------------------------------------------------
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]

        # Shake timer--------------------------------------------------------------------
        self.shake_timer = 0

        # Player-------------------------------------------------------------------------
        self.player = Player(WINDOW_WIDTH - PLAYER_WIDTH, 0)

        # Wand---------------------------------------------------------------------------
        self.wand = Wand(self.player.rect.centerx, self.player.rect.centery)

        # Enemy--------------------------------------------------------------------------
        self.ground_enemy = Enemy(0, 0)

        # Flying Enemy-------------------------------------------------------------------
        self.flying_enemy = FlyingEnemy(50, 0)

        # Shooting Enemy-----------------------------------------------------------------
        self.shooting_enemy = ShootingEnemy(250, 0)

        # Bullet group-------------------------------------------------------------------
        self.bullet_group = CustomGroup()

        # Enemy Bullet group-------------------------------------------------------------
        self.enemy_bullet_group = CustomGroup()

        # For background particles-------------------------------------------------------
        self.background_particles = []

        # For sparks---------------------------------------------------------------------
        self.sparks = []

        # For particles------------------------------------------------------------------
        self.particles = []

        # For falling particles----------------------------------------------------------
        self.falling_particles = []

        # For radiation------------------------------------------------------------------
        self.radiations = []

        # For walking enemies------------------------------------------------------------
        self.all_ground_enemies = CustomGroup(self.ground_enemy)

        # For flying enemies------------------------------------------------------------
        self.all_flying_enemies = CustomGroup(self.flying_enemy, self.shooting_enemy)

        # For shooting enemies----------------------------------------------------------
        self.all_shooting_enemies = CustomGroup(self.shooting_enemy)

        # Function before starting game loop
        # Function for creating tile-----------------------------------------------------
        create_tiles()

        # Function for creating background----------------------------------------------
        load_bg_images()

        # Function for loading background images----------------------------------------
        load_long_rocks()

        # For every sprite when collided with bullet it will create spark---------------
        self.all_sprites_group = pygame.sprite.Group(tiles_group, self.all_ground_enemies, self.all_flying_enemies, self.all_shooting_enemies)

        # For shooting enemy when enemy bullet hits player and tiles--------------------
        self.enemy_hits = pygame.sprite.Group(tiles_group, pygame.sprite.Group(self.player))

    
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

            # Drawing of bullets
            self.bullet_group.update(dt, self.scroll)
            self.bullet_group.draw(display, self.scroll)

            # Update and draw methods of enemy bullet groups
            self.enemy_bullet_group.update(dt, self.scroll)
            self.enemy_bullet_group.draw(display, self.scroll)

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

            # Enemmy update and render
            self.ground_enemy.update(dt, self.scroll, self.player)
            self.ground_enemy.render(self.scroll)

            # Flying Enemy update and render
            self.flying_enemy.update(self.player, dt)
            self.flying_enemy.render(self.scroll)

            # Shooting Enemy update and render
            self.shooting_enemy.update(self.enemy_bullet_group, self.player, self.scroll, dt)
            self.shooting_enemy.render(self.scroll)

            # Drawing particles
            self.draw_floating_particles()

            # Drawing falling particles
            self.draw_falling_particles()

            # Drawing radiation
            self.draw_radiations()

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

    def shoot_bullet(self, previous_time, player_rect_centerx, player_rect_centery):
        mouse_hold = pygame.mouse.get_pressed()
        if mouse_hold[0]:
            current_time = pygame.time.get_ticks()
            if current_time - previous_time[0] > SHOOTING_COOLDOWN:

                mouse_x = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH) + self.scroll[0]
                mouse_y = (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT) + self.scroll[1]
                
                bullet = Bullet("assets/images/bullet.png", 
                                player_rect_centerx, 
                                player_rect_centery, 
                                self.player.x_direction, 
                                mouse_x,
                                mouse_y)
                self.bullet_group.add(bullet)
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
        hits = pygame.sprite.groupcollide(self.bullet_group, self.all_sprites_group, False, False)

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
        for _ in range(10): # location, velocity, radius, color
            self.particles.append([[random.randrange(pos[0]-30, pos[0]+30), random.randrange(pos[1]-20, pos[1]+20)],
                                    [random.randrange(-3, 3), -2], 
                                    random.randrange(24, 30),
                                    255])
    
    def create_falling_particles(self):
        hits = pygame.sprite.groupcollide(self.bullet_group, self.all_ground_enemies, True, False)

        for bullet, enemy in hits.items():
            pos = list(bullet.rect.center)
            for _ in range(20): # location, velocity, radius
                self.falling_particles.append([[random.randrange(pos[0]-20, pos[0]+20), random.randrange(pos[1]-20, pos[1]+20)],
                                        [random.randrange(-3, 3), -2], 
                                        random.randrange(10, 14),
                                        255])

    def create_radiation(self):
        hits = pygame.sprite.groupcollide(self.bullet_group, self.all_flying_enemies, True, False)

        for bullet, enemy in hits.items():
            pos = list(bullet.rect.center)
            # location, radius, width
            self.radiations.append([[pos[0], pos[1]],
                                    15,
                                    8])

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
                particle[1][1] += .001

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
                                   (78, 45, 145),
                                   (particle[0][0] - self.scroll[0], particle[0][1] - self.scroll[1]),
                                   int(particle[2]))

    def draw_radiations(self):
        if self.radiations:
            self.radiations = [radiation for radiation in self.radiations if radiation[2] > 1.1]

            for radiation in self.radiations:
                radiation[1] += 6 # radius
                radiation[2] -= .1 # width
                pygame.draw.circle(display,
                                   (81, 143, 85),
                                   (radiation[0][0]-self.scroll[0], radiation[0][1]-self.scroll[1]), int(radiation[1]),
                                   int(radiation[2]))