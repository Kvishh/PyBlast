import pygame
from configs import *
from game_map import tiles_blocks
import effects_sytem as fx
from tank import Tank
from light import Light
from flight import Flight
from soar import Soar
from shoot import Shoot
from burst import Burst
from specter import Specter

def collide_rect_then_mask(sprite1, sprite2):
    if not sprite1.rect.colliderect(sprite2.rect): return False

    return True if pygame.sprite.collide_mask(sprite1, sprite2) else False

def collide_rect_then_mask_with_piercing_fx(sprite1, sprite2):
    if sprite2 not in sprite1.enemies_hit:

        if not sprite1.rect.colliderect(sprite2.rect):
            return False

        if pygame.sprite.collide_mask(sprite1, sprite2):
            sprite1.enemies_hit[sprite2] = False
            return True 
        else:
            return False

def avoid_overlap(all_ground_enemies):
    for x in all_ground_enemies:
        for y in all_ground_enemies:
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


def player_bullet_hit_all_enemies(player, hud, xp_increment, enemies_killed, player_bullet_group, all_enemies_that_can_be_hit_by_playerbullet_group, shake_timer):
    hits = pygame.sprite.groupcollide(player_bullet_group, all_enemies_that_can_be_hit_by_playerbullet_group, False, False, collide_rect_then_mask_with_piercing_fx)

    for bullet, enemies in hits.items():
        shake_timer[0] = 20
        pos = list(bullet.rect.center)
        
        for enemy in enemies:
            enemy.is_hit = True
            enemy.flashed_timer = pygame.time.get_ticks()

            enemy.hp -= player.damage
                
            if enemy.hp <= 0:
                enemies_killed.add(enemy)
                xp_increment = 80 - (hud.level*10)
                hud.update_level_bar(xp_increment)

        fx.create_impacts(pos)
        fx.create_floating_particles(pos)

def projectiles_hit_player(player, wand, all_enemy_projectiles_that_hit_player, shake_timer):
    if not player.is_invincible:
        tiles_offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        player_tile_loc = (int(player.rect.x // TILE_SIZE), int(player.rect.y // TILE_SIZE))
        player_grid_locs = {f"{player_tile_loc[0] + offset[0]};{player_tile_loc[1] + offset[1]}" for offset in tiles_offset}

        for projectile in all_enemy_projectiles_that_hit_player:
            projectile_tile_loc = (int(projectile.rect.x // TILE_SIZE), int(projectile.rect.y // TILE_SIZE))

            for offset in tiles_offset:
                check_loc = str(projectile_tile_loc[0] + offset[0]) + ";" + str(projectile_tile_loc[1] + offset[1])
                if check_loc in player_grid_locs:
                    if projectile.rect.colliderect(player.rect):
                        if pygame.sprite.collide_mask(projectile, player):
                            player.current_hp -= 1
                            player.invincible_timer = pygame.time.get_ticks()
                            player.is_invincible = True

                            wand.invincible_timer = pygame.time.get_ticks()
                            wand.is_invincible = True

                            shake_timer[0] = 20
                            pos = list(projectile.rect.center)
                            fx.create_impacts(pos)
                            fx.create_floating_particles(pos)
                            projectile.kill()
                            break

def all_enemies_touch_player(player, wand, all_enemies_group):
    if not player.is_invincible:
        hits = pygame.sprite.spritecollide(player, all_enemies_group, False, collide_rect_then_mask)

        for enemy in hits:
            player.current_hp -= 1
            player.invincible_timer = pygame.time.get_ticks()
            player.is_invincible = True

            wand.invincible_timer = pygame.time.get_ticks()
            wand.is_invincible = True

def projectiles_hit_tiles(all_projectile_that_hit_tiles, shake_timer):
    # collided_tiles_loc = []
    tiles_offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    for projectile in all_projectile_that_hit_tiles.sprites():
        projectile_tile_loc = (int(projectile.rect.x // TILE_SIZE), int(projectile.rect.y // TILE_SIZE))
        for offset in tiles_offset:
            check_loc = str(projectile_tile_loc[0] + offset[0]) + ";" + str(projectile_tile_loc[1] + offset[1])
            if check_loc in tiles_blocks:
                collided_tile = tiles_blocks[check_loc]
                if collided_tile.rect.colliderect(projectile.rect):
                    shake_timer[0] = 20
                    pos = list(projectile.rect.center)
                    fx.create_debris(pos)
                    fx.create_impacts(pos)
                    fx.create_floating_particles(pos)
                    projectile.kill()

def player_bullet_hit_flying_enemies(player_bullet_group):
    for bullet in player_bullet_group.sprites():
        for enemy in bullet.enemies_hit:
            if isinstance(enemy, (Flight, Soar, Shoot, Burst, Specter)):
                pos = list(bullet.rect.center)

                if not bullet.enemies_hit[enemy]:
                    fx.create_radiation(enemy, pos)
                    bullet.enemies_hit[enemy] = True
                
                if len(bullet.enemies_hit) >= bullet.pierce_number:
                    bullet.kill()

def player_bullet_hit_ground_enemies(player_bullet_group):
    for bullet in player_bullet_group.sprites():
        for enemy in bullet.enemies_hit:
            if isinstance(enemy, (Tank, Light)):
                pos = list(bullet.rect.center)

                if not bullet.enemies_hit[enemy]:
                    fx.create_falling_particles(enemy, pos)
                    bullet.enemies_hit[enemy] = True
                
                if len(bullet.enemies_hit) >= bullet.pierce_number:
                    bullet.kill()