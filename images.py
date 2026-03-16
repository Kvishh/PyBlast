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

class TileImage:
    tile_image = pygame.image.load("assets/images/tile1.png").convert_alpha()
    tile_image_scaled = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))

class BackgroundImages:
    bg_images_list = [pygame.image.load(f"assets/images/bg_{i}.png").convert_alpha() for i in range(1, 5)]

class LongRocksImages:
    long_rock_1_image = pygame.image.load("assets/images/long_rock1.png").convert_alpha() # for 1 and 3
    long_rock_2_image = pygame.image.load("assets/images/long_rock2.png").convert_alpha()
    long_rock_4_image = pygame.transform.rotate(pygame.transform.flip(pygame.image.load("assets/images/long_rock2.png").convert_alpha(), True, False), 10)

    long_rocks_list = [long_rock_1_image,long_rock_2_image,long_rock_1_image,long_rock_4_image]

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

    light_image_flashed_white = pygame.transform.flip(pygame.image.load("assets/images/slime_flashed_white.png").convert_alpha(), True, False)
    light_image_flashed_white_scaled = pygame.transform.scale(light_image_flashed_white, (LIGHT_ENEMY_WIDTH, LIGHT_ENEMY_HEIGHT))
    light_image_flashed_white_scaled_flipped = pygame.transform.flip(light_image_flashed_white_scaled, True, False)

class TankImages:
    tank_image = pygame.image.load("assets/images/tank.png").convert_alpha()
    tank_image_scaled = pygame.transform.scale(tank_image, (HEAVY_ENEMY_WIDTH, HEAVY_ENEMY_HEIGHT))
    tank_image_scaled_flipped = pygame.transform.flip(tank_image_scaled, True, False)

    tank_run_animations_frames_list = load_animation("assets/images/tank_animation.png", 1, 3, 28, 32, HEAVY_ENEMY_WIDTH, HEAVY_ENEMY_HEIGHT)
    tank_run_animations_frames_flipped_list = [pygame.transform.flip(frame, True, False) for frame in tank_run_animations_frames_list]

    tank_run_animations_flashed_white_frames_list = load_animation("assets/images/tank_animation_flashed_white.png", 1, 3, 28, 32, HEAVY_ENEMY_WIDTH, HEAVY_ENEMY_HEIGHT)
    tank_run_animations_flashed_white_frames_flipped_list = [pygame.transform.flip(frame, True, False) for frame in tank_run_animations_flashed_white_frames_list]

class FlightImage:
    flight_image = pygame.image.load("assets/images/flight.png").convert_alpha()
    flight_image_scaled = pygame.transform.scale(flight_image, (FLIGHT_ENEMY_WIDTH, FLIGHT_ENEMY_HEIGHT))
    flight_image_scaled_flipped = pygame.transform.flip(flight_image_scaled, True, False)

    flight_run_animations_frames_list = load_animation("assets/images/flight_animation.png", 1, 3, 18, 20, FLIGHT_ENEMY_WIDTH, FLIGHT_ENEMY_HEIGHT)
    flight_run_animations_frames_flipped_list = [pygame.transform.flip(frame, True, False) for frame in flight_run_animations_frames_list]

    flight_run_animations_flashed_white_frames_list = load_animation("assets/images/flight_animation_flashed_white.png", 1, 3, 18, 20, FLIGHT_ENEMY_WIDTH, FLIGHT_ENEMY_HEIGHT)
    flight_run_animations_flashed_white_frames_flipped_list = [pygame.transform.flip(frame, True, False) for frame in flight_run_animations_flashed_white_frames_list]

class SoarImage:
    soar_image = pygame.image.load("assets/images/soar.png").convert_alpha()
    soar_image_scaled = pygame.transform.scale(soar_image, (SOAR_ENEMY_WIDTH, SOAR_ENEMY_HEIGHT))
    soar_image_scaled_flipped = pygame.transform.flip(soar_image_scaled, True, False)

    soar_image_flashed_white = pygame.image.load("assets/images/soar_flashed_white.png").convert_alpha()
    soar_image_flashed_white_scaled = pygame.transform.scale(soar_image_flashed_white, (SOAR_ENEMY_WIDTH, SOAR_ENEMY_HEIGHT))
    soar_image_flashed_white_scaled_flipped = pygame.transform.flip(soar_image_flashed_white_scaled, True, False)

class ShootImage:
    shoot_image = pygame.image.load("assets/images/shoot.png").convert_alpha()
    shoot_image_scaled = pygame.transform.scale(shoot_image, (SHOOTING_ENEMY_WIDTH, SHOOTING_ENEMY_HEIGHT))

    shoot_flashed_white_image = pygame.image.load("assets/images/shoot_flashed_white.png").convert_alpha()
    shoot_flashed_white_image_scaled = pygame.transform.scale(shoot_flashed_white_image, (SHOOTING_ENEMY_WIDTH, SHOOTING_ENEMY_HEIGHT))

class BurstImage:
    burst_image = pygame.image.load("assets/images/burst.png").convert_alpha()
    burst_image_scaled = pygame.transform.scale(burst_image, (BURST_ENEMY_WIDTH, BURST_ENEMY_HEIGHT))

    burst_flashed_white_image = pygame.image.load("assets/images/burst_flashed_white.png").convert_alpha()
    burst_flashed_white_image_scaled = pygame.transform.scale(burst_flashed_white_image, (BURST_ENEMY_WIDTH, BURST_ENEMY_HEIGHT))

class SpecterImage:
    specter_image = pygame.image.load("assets/images/specter.png").convert_alpha()
    specter_image_scaled = pygame.transform.scale(specter_image, (SPECTER_ENEMY_WIDTH, SPECTER_ENEMY_HEIGHT))

    specter_flashed_white_image = pygame.image.load("assets/images/specter_flashed_white.png").convert_alpha()
    specter_flashed_white_image_scaled = pygame.transform.scale(specter_flashed_white_image, (SPECTER_ENEMY_WIDTH, SPECTER_ENEMY_HEIGHT))