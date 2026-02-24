import pygame, random, math
from configs import *
from game_map import tiles_group, draw_background, create_tiles, load_bg_images, load_long_rocks, draw_tiles, draw_behind_long_rocks, draw_front_long_rocks
from player import Player
from wand import Wand
from bullet import Bullet
from customgroup import CustomGroup
from enemy import Enemy
from spark import Spark

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # GAME COMPONENTS----------------------------------------------------------------
        # Scrolling (Camera effect)------------------------------------------------------
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]

        # Player-------------------------------------------------------------------------
        self.player = Player(0, 0)

        # Wand---------------------------------------------------------------------------
        self.wand = Wand(self.player.rect.centerx, self.player.rect.centery)

        # Enemy--------------------------------------------------------------------------
        self.enemy = Enemy(0, 0)

        # Bullet group-------------------------------------------------------------------
        self.bullet_group = CustomGroup()

        # For background particles-------------------------------------------------------
        self.background_particles = []

        # For sparks---------------------------------------------------------------------
        self.sparks = []

        # For particles------------------------------------------------------------------
        self.particles = []

        # For walking enemies------------------------------------------------------------
        self.all_enemies = CustomGroup(self.enemy)

        # Function before starting game loop
        # Function for creating tile-----------------------------------------------------
        create_tiles()

        # Function for creating background----------------------------------------------
        load_bg_images()

        # Function for loading background images----------------------------------------
        load_long_rocks()

        # For every sprite when collided with bullet it will create spark---------------
        self.all_sprites_group = pygame.sprite.Group(tiles_group, self.all_enemies)

    
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

            # For drawing background
            draw_background(self.scroll)

            # Drawing behind platforms but in front of background
            draw_behind_long_rocks(self.scroll)

            # For drawing tiles
            draw_tiles(self.scroll)

            # Creating background particles
            self.create_background_particles()
            
            # Player and Wand update and draw methods
            self.wand.update(self.player, self.scroll, self.player.rect.centerx, self.player.rect.centery)
            self.wand.render(self.scroll)
            self.player.update(pygame.key.get_pressed(), dt)
            self.player.render(self.scroll)

            # Enemmy update and render
            self.enemy.update(dt, self.scroll, self.player)
            self.enemy.render(self.scroll)

            # Checking of mouse hold and creation of bullet
            self.shoot_bullet(previous_time, self.player.rect.centerx, self.player.rect.centery)

            # Drawing of bullets
            self.bullet_group.update(dt, self.scroll)
            self.bullet_group.draw(display, self.scroll)

            # Creating and drawing sparks
            self.create_impact()
            self.draw_impact()

            # Drawing particlels
            self.draw_particles()

            # Rendering of front objects (long rocks)
            draw_front_long_rocks(self.scroll)

            # Drawing background particles
            self.draw_background_particles()

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

    def create_impact(self):
        hits = pygame.sprite.groupcollide(self.bullet_group, self.all_sprites_group, True, False)

        for bullet, collided_sprites in hits.items():
            self.create_particles(bullet.rect.center)

            for _ in range(6):
                self.sparks.append(Spark([bullet.rect.centerx, bullet.rect.centery], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))
    
    def draw_impact(self):
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.move(1)
            spark.draw(display, self.scroll)
            if not spark.alive:
                self.sparks.pop(i)

    def create_particles(self, pos):
        pos = list(pos)
        for _ in range(10): # location, velocity, radius, color
            self.particles.append([[random.randrange(pos[0]-30, pos[0]+30), random.randrange(pos[1]-20, pos[1]+20)],
                                    [random.randrange(-2, 2), -2], 
                                    random.randrange(8, 12),
                                    255])
    
    def draw_particles(self):
        if self.particles:
            self.particles = [particle for particle in self.particles if particle[2] > 0]

            for particle in self.particles:
                # radius decrement
                particle[2] -= .1

                # change position over time
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]

                # change y velocity over time
                particle[1][1] += .1

                # change color over time
                particle[3] -= 2
                pygame.draw.circle(display,
                                   (int(particle[3]), int(particle[3]), int(particle[3])),
                                   (particle[0][0] - self.scroll[0], particle[0][1] - self.scroll[1]),
                                   int(particle[2]))
