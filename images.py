import pygame
from configs import *

def load_animation(file, row, col, width, height, scale_width, scale_height):
    sprites_list = []

    spritesheet = pygame.image.load(file).convert_alpha()

    for i in range(row):
        for j in range(col):
            x = j * width # 21 is frame width for player idle
            y = i * height # 24 is frame height for player idle
            frame = spritesheet.subsurface((x, y, width, height))
            frame = pygame.transform.scale(frame, (scale_width, scale_height))
            sprites_list.append(frame)
    
    return sprites_list

class GradientImage:
    gradient_image = pygame.image.load("assets/images/radial_gradient.png").convert()
    gradient_player_image_scaled = pygame.transform.scale(pygame.image.load("assets/images/radial_gradient.png").convert(), (270, 270))

class PlayerImages:
    player_image = pygame.image.load("assets/images/main_sorcerer.png").convert_alpha()
    player_image_scaled = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
    player_image_scaled_flipped = pygame.transform.flip(player_image_scaled, True, False)

    player_idle_animations_frames_list = load_animation("assets/images/player_animation_idle.png", 1, 2, 21, 24, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_idle_animations_frames_flipped_list = [pygame.transform.flip(frame, True, False) for frame in player_idle_animations_frames_list]

    player_run_animations_frames_list = load_animation("assets/images/player_animation_run.png", 1, 3, 21, 24, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_run_animations_frames_flipped_list = [pygame.transform.flip(frame, True, False) for frame in player_run_animations_frames_list]

class WandImage:
    wand_image = pygame.image.load("assets/images/player_wand.png").convert_alpha()
    wand_image_rotated = pygame.transform.rotate(wand_image, -90)

class BulletImage:
    bullet_image = pygame.image.load("assets/images/bullet.png").convert_alpha()
    bullet_image_scaled = pygame.transform.scale(bullet_image, (BULLET_SIZE, BULLET_SIZE))

class EnemyBulletImage:
    enemy_bullet_image = pygame.image.load("assets/images/enemy_projectile.png").convert_alpha()
    enemy_bullet_image_scaled = pygame.transform.scale(enemy_bullet_image, (BULLET_SIZE, BULLET_SIZE))

class SpecterEnemyBulletImage:
    specter_enemy_bullet_image = pygame.image.load("assets/images/enemy_projectile.png").convert_alpha()
    specter_enemy_bullet_image_scaled = pygame.transform.scale(specter_enemy_bullet_image, (BULLET_SIZE, BULLET_SIZE))

class LightImage:
    light_image = pygame.transform.flip(pygame.image.load("assets/images/slime.png").convert_alpha(), True, False) # original image facing left, flipped to face right
    light_image_scaled = pygame.transform.scale(light_image, (LIGHT_ENEMY_WIDTH, LIGHT_ENEMY_HEIGHT))
    light_image_scaled_flipped = pygame.transform.flip(light_image_scaled, True, False)

class TankImages:
    tank_image = pygame.image.load("assets/images/tank.png").convert_alpha()
    tank_image_scaled = pygame.transform.scale(tank_image, (HEAVY_ENEMY_WIDTH, HEAVY_ENEMY_HEIGHT))
    tank_image_scaled_flipped = pygame.transform.flip(tank_image_scaled, True, False)

    tank_run_animations_frames_list = load_animation("assets/images/tank_animation.png", 1, 3, 28, 32, HEAVY_ENEMY_WIDTH, HEAVY_ENEMY_HEIGHT)
    tank_run_animations_frames_flipped_list = [pygame.transform.flip(frame, True, False) for frame in tank_run_animations_frames_list]

class FlightImage:
    flight_image = pygame.image.load("assets/images/flight.png").convert_alpha()
    flight_image_scaled = pygame.transform.scale(flight_image, (FLIGHT_ENEMY_WIDTH, FLIGHT_ENEMY_HEIGHT))
    flight_image_scaled_flipped = pygame.transform.flip(flight_image_scaled, True, False)

    flight_run_animations_frames_list = load_animation("assets/images/flight_animation.png", 1, 3, 18, 20, FLIGHT_ENEMY_WIDTH, FLIGHT_ENEMY_HEIGHT)
    flight_run_animations_frames_flipped_list = [pygame.transform.flip(frame, True, False) for frame in flight_run_animations_frames_list]