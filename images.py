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