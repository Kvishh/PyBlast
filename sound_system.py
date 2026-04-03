import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(64)

class SFX:
    player_hit_sfx = pygame.mixer.Sound("assets/sfx/player_hit_sfx.wav")
    player_hit_sfx.set_volume(.8)

    player_bullet_fire_sfx = pygame.mixer.Sound("assets/sfx/player_bullet_fire_sfx.wav")
    player_bullet_fire_sfx.set_volume(.13)

    enemies_bullet_fire_sfx = pygame.mixer.Sound("assets/sfx/enemies_bullet_fire_sfx.wav")
    enemies_bullet_fire_sfx.set_volume(.2)

    normal_bullet_hit_enemies_sfx = pygame.mixer.Sound("assets/sfx/normal_player_bullet_hit_enemies_sfx.wav")
    normal_bullet_hit_enemies_sfx.set_volume(.3)

    bullet_explosion_sfx = pygame.mixer.Sound("assets/sfx/player_bullet_explosion_sfx.wav")
    bullet_explosion_sfx.set_volume(.3)

    projectile_hit_tiles_sfx = pygame.mixer.Sound("assets/sfx/projectiles_hit_tiles_sfx.wav")
    projectile_hit_tiles_sfx.set_volume(.3)

    enemies_projectiles_hit_negator_sfx = pygame.mixer.Sound("assets/sfx/negator_hit_sfx.wav")
    enemies_projectiles_hit_negator_sfx.set_volume(.3)

    walk_sfx_list = [pygame.mixer.Sound("assets/sfx/walk1_sfx.wav"), pygame.mixer.Sound("assets/sfx/walk2_sfx.wav")]
    walk_sfx_list[0].set_volume(.15)
    walk_sfx_list[1].set_volume(.15)

    jump_sfx = pygame.mixer.Sound("assets/sfx/jump_sfx.wav")
    jump_sfx.set_volume(.2)

    dash_sfx = pygame.mixer.Sound("assets/sfx/dash_sfx.wav")
    dash_sfx.set_volume(.2)

    level_up_sfx = pygame.mixer.Sound("assets/sfx/level_up_sfx.wav")
    level_up_sfx.set_volume(.2)

class Music:
    battle_music = "assets/bg_music/battle_music_1.wav"
    menu_music = "assets/bg_music/Falling to Earth (Loop).wav"

    def play_music(path, volume=.2, fade_ms=500):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1, fade_ms=fade_ms)
        pygame.mixer.music.set_volume(volume)
    
    def stop_music(fadeout_ms=500):
        pygame.mixer.music.fadeout(fadeout_ms)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()