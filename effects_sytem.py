import pygame, math, random
from configs import *
from game_map import tiles_blocks
from images import GradientImage
from spark import Spark
from tank import Tank
from light import Light
from flight import Flight
from soar import Soar
from shoot import Shoot
from burst import Burst
from specter import Specter


class FxList:
    """Class for storing the effects list."""

    # For background particles---------------------------------------------------------------------------------
    background_particles = []

    # For sparks-----------------------------------------------------------------------------------------------
    sparks = []

    # For explosion sparks-------------------------------------------------------------------------------------
    explosion_sparks = []

    # For explosion -------------------------------------------------------------------------------------------
    explosions = []

    # For explosion radiations---------------------------------------------------------------------------------
    explosion_radiations = []

    # For particles--------------------------------------------------------------------------------------------
    particles = []

    # For falling particles------------------------------------------------------------------------------------
    falling_particles = []

    # For radiation--------------------------------------------------------------------------------------------
    radiations = []

    # For debris------------------------------------------------------------------------------------------------
    debris = []

    # For jump particles----------------------------------------------------------------------------------------
    jump_particles = []



def create_background_particles():
    """Creation of the fireflies/background particles"""

    if len(FxList.background_particles) < 10: # loc, radius, direction
        FxList.background_particles.append([[random.randrange(WINDOW_WIDTH), random.randrange(WINDOW_HEIGHT)],
                                    2,
                                    # [random.choice([random.uniform(.4, .6), random.uniform(-.4, -.6)]), random.choice([random.uniform(.4, .6), random.uniform(-.4, -.6)])],
                                    [random.choice([random.uniform(40.4, 40.6), random.uniform(-40.4, -40.6)]), random.choice([random.uniform(40.4, 40.6), random.uniform(-40.4, -40.6)])],
                                    random.choice(GradientImage.gradient_background_image_list)])

def draw_background_particles(dark_overlay, scroll, dt):
    """Drawing of the fireflies/background particles"""

    if FxList.background_particles:
        FxList.background_particles = [background_particle for background_particle in FxList.background_particles
                                if (background_particle[0][1] > 0 and background_particle[0][1] < WINDOW_HEIGHT) and 
                                (background_particle[0][0] > 0 and background_particle[0][0] < WINDOW_WIDTH)]            
        
        # loc, radius, direction
        for bg_particle in FxList.background_particles:
            bg_particle[0][0] += bg_particle[2][0] * dt
            bg_particle[0][1] += bg_particle[2][1] * dt
            """Movement of particle"""

            gradient_copy = bg_particle[3]
            dark_overlay.blit(gradient_copy,
                                    (bg_particle[0][0]-scroll[0] - (gradient_copy.get_rect().w//2),
                                    bg_particle[0][1]-scroll[1] - (gradient_copy.get_rect().h//2)),
                                    special_flags=pygame.BLEND_RGBA_ADD)
            """The two lines above are responsible for the gradient image"""

            pygame.draw.circle(display, (255, 255, 255), [int(bg_particle[0][0])-scroll[0], int(bg_particle[0][1])-scroll[1]], bg_particle[1])
            """The line above is for the white opaque circle"""

            radius = 35 # if gradient_image w and h is 70
            r_increment = -1 # if gradient_image w and h is 70
            gradient_image_w = gradient_copy.get_rect().w
            if gradient_image_w == 90:
                radius = 45
                r_increment = 5

            layer1 = pygame.Surface((radius,radius))
            layer1.set_colorkey((0,0,0))

            for i in range(2, -1, -1):
                c = 30 - i*10 * 4
                c = pygame.math.clamp(c, 5, 255)
                r = r_increment + (i*5) + 8
                pygame.draw.circle(layer1, (c,c,c), layer1.get_rect().center, r)

            display.blit(layer1,
                            ((bg_particle[0][0]-scroll[0]) - (layer1.get_rect().w//2),
                            (bg_particle[0][1]-scroll[1]) - (layer1.get_rect().h//2)),
                            special_flags=pygame.BLEND_RGBA_ADD)


def create_floating_particles(pos):
    """Creation of the fireflies/background particles"""

    for _ in range(15): # location, velocity, radius, color
        FxList.particles.append([[random.randrange(pos[0]-30, pos[0]+30), random.randrange(pos[1]-20, pos[1]+20)],
                                [random.randrange(-4, 4), -5], 
                                random.randrange(16, 20),
                                255])

def draw_floating_particles(scroll):
    """Drawing of floating """

    if FxList.particles:
        FxList.particles = [particle for particle in FxList.particles if particle[2] > 0]

        for particle in FxList.particles:
            # radius decrement
            particle[2] -= 1

            # change position over time
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]

            # change y velocity over time
            particle[1][1] += .02

            # change color over time
            particle[3] -= random.randint(1, 3)
            pygame.draw.circle(display,
                                (int(particle[3]), int(particle[3]), int(particle[3])),
                                (particle[0][0] - scroll[0], particle[0][1] - scroll[1]),
                                int(particle[2]))

            # rad = int(particle[2])
            # if rad > 0:
            #     surf = self.get_cached_particle(rad, (particle[3],particle[3],particle[3]))
            #     display.blit(surf, (particle[0][0]-self.scroll[0], particle[0][1]-self.scroll[1]))


def create_falling_particles(enemy, pos):
    """Creation of the falling particles when any of the ground enemies is hit."""

    if isinstance(enemy, Light):
        for _ in range(15): # location, velocity, radius, color
            FxList.falling_particles.append([[random.randrange(pos[0]-20, pos[0]+20), random.randrange(pos[1]-20, pos[1]+20)],
                                    [random.randrange(-3, 3), -2], 
                                    random.randrange(10, 14),
                                    (78, 45, 145)])
    elif isinstance(enemy, Tank):
        for _ in range(15): # location, velocity, radius
            FxList.falling_particles.append([[random.randrange(pos[0]-20, pos[0]+20), random.randrange(pos[1]-20, pos[1]+20)],
                                    [random.randrange(-3, 3), -2], 
                                    random.randrange(10, 14),
                                    (155, 86, 186)])

def draw_falling_particles(scroll):
    """Drawing of falling particles."""

    if FxList.falling_particles:
        FxList.falling_particles = [particle for particle in FxList.falling_particles if particle[2] > 0]

        for particle in FxList.falling_particles:
            # radius decrement
            particle[2] -= .2

            # change position over time
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]

            # change y velocity over time
            particle[1][1] += .2

            pygame.draw.circle(display,
                                (32, 33, 48),
                                (particle[0][0] + 3 - scroll[0], particle[0][1] + 3 - scroll[1]),
                                int(particle[2]))

            pygame.draw.circle(display,
                                particle[3],
                                (particle[0][0] - scroll[0], particle[0][1] - scroll[1]),
                                int(particle[2]))


def create_debris(pos):
    """Creation of debris when projectiles hit tiles."""

    for _ in range(15):  # location, velocity, radius, color
        r = random.randrange(60, 80)
        g = r
        FxList.debris.append([[pos[0], pos[1]], # x axis random.randrange(pos[0]-20, pos[0]+20) ; y axis random.randrange(pos[1]-20, pos[1]+20)
                    [random.randrange(-3, 3), random.randrange(-3, 3)], 
                    random.randrange(8, 12),
                    (r, g, 125)])

def draw_debris(scroll):
    """Drawing of the debris."""

    if FxList.debris:
        FxList.debris = [debris for debris in FxList.debris if debris[2] > 0]

        for debris in FxList.debris:
            # radius decrement
            debris[2] -= .2

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
                                (debris[0][0] + 5 - scroll[0], debris[0][1] + 5 - scroll[1]),
                                debris[2])

            pygame.draw.circle(display,
                                debris[3],
                                (debris[0][0] - scroll[0], debris[0][1] - scroll[1]),
                                debris[2])


def create_radiation(enemy, pos):
    """Creation of radiations when any of flying enemies is hit."""

    if isinstance(enemy, Soar):
        FxList.radiations.append([[pos[0], pos[1]],
                                15,
                                13,
                                1,
                                (152, 0, 212)])

        FxList.radiations.append([[pos[0], pos[1]],
                                15,
                                8,
                                0,
                                [(152, 0, 212), (82, 27, 27)]])
    elif isinstance(enemy, Flight):
        FxList.radiations.append([[pos[0], pos[1]],
                                4,
                                8,
                                3,
                                [(199, 48, 115), (105, 41, 71)]])
    elif isinstance(enemy, Shoot):
        FxList.radiations.append([[pos[0], pos[1]],
                                15,
                                8,
                                0,
                                [(203, 0, 255), (71, 36, 82)]])
    elif isinstance(enemy, Burst):
        FxList.radiations.append([[pos[0], pos[1]],
                                15,
                                8,
                                0,
                                [(165, 0, 207), (71, 36, 82)]])
    elif isinstance(enemy, Specter):
        FxList.radiations.append([[pos[0], pos[1]],
                                15,
                                8,
                                0,
                                [(114, 0, 143), (71, 36, 82)]])

def draw_radiations(scroll):
    """Drawing of the radiations."""

    if FxList.radiations:
        FxList.radiations = [radiation for radiation in FxList.radiations if radiation[2] > 1.1]

        for radiation in FxList.radiations:
            if radiation[3] == 1:
                radiation[1] += 12 # radius
                radiation[2] -= .4 # width

                if radiation[2] < 1: radiation[2] = 1

                pygame.draw.circle(display,
                                radiation[4],
                                (radiation[0][0] - scroll[0], radiation[0][1] - scroll[1]), int(radiation[1]),
                                int(radiation[2]))
            elif radiation[3] == 3:
                radiation[1] += 3 # radius
                radiation[2] -= .2 # width

                if radiation[2] < 1: radiation[2] = 1

                pygame.draw.circle(display,
                                radiation[4][1],
                                (radiation[0][0] + 6 - scroll[0], radiation[0][1] + 3 - scroll[1]), int(radiation[1]),
                                int(radiation[2]))

                pygame.draw.circle(display,
                                radiation[4][0],
                                (radiation[0][0]-scroll[0], radiation[0][1]-scroll[1]), int(radiation[1]),
                                int(radiation[2]))
            else:
                radiation[1] += 7 # radius
                radiation[2] -= .2 # width

                if radiation[2] < 1: radiation[2] = 1

                pygame.draw.circle(display,
                                radiation[4][1],
                                (radiation[0][0] + 6 - scroll[0], radiation[0][1] + 3 - scroll[1]), int(radiation[1]),
                                int(radiation[2]))

                pygame.draw.circle(display,
                                radiation[4][0],
                                (radiation[0][0]-scroll[0], radiation[0][1]-scroll[1]), int(radiation[1]),
                                int(radiation[2]))


def create_impacts(pos):
    """Creation of impacts for normal projectiles that hit tile or enemies."""

    for _ in range(6):
        FxList.sparks.append(Spark([pos[0], pos[1]], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))

def draw_impact(scroll):
    """Drawing of sparks/impacts when projectile hit something."""

    for i, spark in sorted(enumerate(FxList.sparks), reverse=True):
        spark.move(1)
        spark.draw(display, scroll)
        if not spark.alive:
            FxList.sparks.pop(i)

def create_explosion_impacts(pos):
    """Creation of explosion impacts from the explosion when player projectiles hit something"""

    for i in range(13):
        angle = math.pi * 2 * (i/10)
        speed = random.randint(5,7)
        FxList.explosion_sparks.append(Spark([pos[0], pos[1]], angle, speed, (255,255,255), scale=4))
        FxList.explosion_sparks.append(Spark([pos[0], pos[1]], angle-.1, speed-1, (238, 255, 107), scale=4))

def draw_explosion_impact(scroll):
    """Drawing of explosion/sparks when projectiles explode"""

    for i, spark in sorted(enumerate(FxList.explosion_sparks), reverse=True):
        spark.move(1)
        spark.draw(display, scroll)
        if not spark.alive:
            FxList.explosion_sparks.pop(i)


def create_explosion(pos):
    """Creation of the huge green radiation."""

    # location, radius, width, color, new_loc, timer, color # id here if you want
    FxList.explosions.append([[pos[0], pos[1]],
                                       70,
                                       5,
                                       (204, 255, 0),
                                       [0, 0],
                                       [30, 0],
                                       (252, 255, 209)])

def draw_explosions(scroll):
    """Drawing of explosion impact, the one where projectiles explode when enemies hit"""

    if FxList.explosions:
        FxList.explosions = [explosion for explosion in FxList.explosions if explosion[1] > 0]

        for explosion in FxList.explosions:

            if explosion[1] > 40:
                explosion[1] = max(0, explosion[1] - 2)

                pygame.draw.circle(display, (explosion[3]), (explosion[0][0]-scroll[0], explosion[0][1]-scroll[1]), explosion[1], 0)
            else:
                explosion[1] = max(0, explosion[1] - 1)

                for i in range(5):
                    explosion[4][0], explosion[4][1] = explosion[0][0] + random.randint(-20, 20), explosion[0][1] + random.randint(-20, 20)

                    if explosion[5][0] == 0:
                        explosion[5][0] = 30
                        explosion[5][1] += 1

                        explosion[6] = (252, 255, 209) if explosion[5][1] % 2 == 0 else (55, 71, 16)

                    explosion[5][0] -= 1

                    pygame.draw.circle(display, (explosion[6]), (explosion[4][0]-scroll[0], explosion[4][1]-scroll[1]), explosion[1], 0)


def create_explosion_radiations(pos):
    """Creation of the huge green radiation."""

    # location, radius, width
    FxList.explosion_radiations.append([[pos[0], pos[1]],
                                        80,
                                        12])

def draw_explosion_radiations(scroll):
    """Drawing of explosion radiations"""

    if FxList.explosion_radiations:
        FxList.explosion_radiations = [radiation for radiation in FxList.explosion_radiations if radiation[2] > 0]

        for radiation in FxList.explosion_radiations:
            radiation[1] = radiation[1]+4
            radiation[2] -= .2

            if radiation[2] > 1:
                pygame.draw.circle(display, (203, 232, 60), (radiation[0][0]-scroll[0], radiation[0][1]-scroll[1]), radiation[1], int(radiation[2]))


def draw_jump_particles(scroll):
    """Drawing of jump particles of player when it jumps."""

    if FxList.jump_particles:
        FxList.jump_particles = [p for p in FxList.jump_particles if p[2] > 0]

        for particle in FxList.jump_particles:
            particle[2] -= .2
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]

            
            pygame.draw.circle(display,
                            (10, 43, 12),
                            (particle[0][0]-scroll[0] + 3, particle[0][1]-scroll[1] + 3),
                            int(particle[2]))

            pygame.draw.circle(display, (178, 235, 23), (particle[0][0] - scroll[0], particle[0][1] - scroll[1]), particle[2])