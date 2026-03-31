import pygame
from configs import *
from game_map import tiles_blocks
from images import ExplosionSurface
import effects_sytem as fx
from tank import Tank
from light import Light
from flight import Flight
from soar import Soar
from shoot import Shoot
from burst import Burst
from specter import Specter

class Timer:
    projectiles_hit_player_invincible_timer = 0
    projectiles_hit_wand_invincible_timer = 0
    enemies_touch_player_invincible_timer = 0
    enemies_touch_wand_invincible_timer = 0

    dt_multiplier = 1

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

def slow_down_time(player, all_enemy_projectiles_that_hit_player, dt):
    for bullet in all_enemy_projectiles_that_hit_player.sprites():
        if bullet.rect.colliderect(player.slow_rect):
            # This is responsible for slowing down movement smoothly
            # Smooth in effect
            Timer.dt_multiplier = max(0.25, Timer.dt_multiplier - .1)
            dt = max(0.0038, dt * Timer.dt_multiplier)
            return dt

    # This is to smooth out the time if enemies' projectiles
    # have gone past through player's radius where slow movement
    # will take effect
    Timer.dt_multiplier = min(1, Timer.dt_multiplier + .018)
    dt = max(0.0038, dt * Timer.dt_multiplier)
    return dt

def check_explosion_radius_rect_collision(explosion_center, radius, rect):
    cx, cy = explosion_center

    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))

    dx = cx - closest_x
    dy = cy - closest_y

    dist_squared = dx**2 + dy**2

    return dist_squared <= radius**2


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
                if hud.level <= 15:
                    xp_increment[0] += 120 - (hud.level*5)
                elif hud.level > 15 and hud.level <= 19:
                    xp_increment[0] += 105 - (hud.level*5)
                elif hud.level >= 20:
                    xp_increment[0] += 10

        fx.create_impacts(pos)
        fx.create_floating_particles(pos)

def check_enemies_within_explosion_radius(player, hud, xp_increment, enemies_killed, player_bullet_group, all_enemies_that_can_be_hit_by_playerbullet_group, shake_timer):
    hits = pygame.sprite.groupcollide(player_bullet_group, all_enemies_that_can_be_hit_by_playerbullet_group, False, False, collide_rect_then_mask_with_piercing_fx)

    enemies_within_radius = set([])
    for bullet in hits.keys():
        pos = bullet.rect.center
        
        shake_timer[0] = 20
        for enemy in all_enemies_that_can_be_hit_by_playerbullet_group.sprites():
            is_within_radius = check_explosion_radius_rect_collision(pos, 70, enemy.hit_rect) if isinstance(enemy, (Shoot, Burst, Specter)) else check_explosion_radius_rect_collision(pos, 70, enemy.rect)

            if is_within_radius: # if true, check for circle enemy mask collision
                explosion_rect = ExplosionSurface.explosion_surf.get_rect(center=(pos[0], pos[1]))

                offset = (enemy.hit_rect.x - explosion_rect.x, enemy.hit_rect.y - explosion_rect.y) if isinstance(enemy, (Shoot, Burst, Specter)) else (enemy.rect.x - explosion_rect.x, enemy.rect.y - explosion_rect.y)

                if ExplosionSurface.explosion_surf_mask.overlap(enemy.mask, offset):
                    enemies_within_radius.add(enemy)
                    fx.create_explosion_impacts(list(pos))
                    fx.create_explosion(list(pos))
                    fx.create_explosion_radiations(list(pos))
    
    for enemy in enemies_within_radius:
        enemy.is_hit = True
        enemy.flashed_timer = pygame.time.get_ticks()

        enemy.hp -= player.damage
            
        if enemy.hp <= 0:
                enemies_killed.add(enemy)
                if hud.level <= 15:
                    xp_increment[0] += 120 - (hud.level*5)
                elif hud.level > 15 and hud.level <= 19:
                    xp_increment[0] += 105 - (hud.level*5)
                elif hud.level >= 20:
                    xp_increment[0] += 10


def projectiles_hit_negator(player, all_enemy_projectiles_that_hit_player):
    hits = pygame.sprite.spritecollide(player.negator, all_enemy_projectiles_that_hit_player, True, collide_rect_then_mask)

def projectiles_hit_player(player, wand, all_enemy_projectiles_that_hit_player, shake_timer, dt):
    Timer.projectiles_hit_player_invincible_timer += dt
    Timer.projectiles_hit_wand_invincible_timer += dt

    if not player.is_invincible and not player.has_survived:
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
                            if player.current_shield != 0:
                                player.current_shield -= 1
                            else:
                                player.current_hp -= 1
                            if player.current_hp <= 0:
                                player.kill()
                                wand.kill()
                            player.invincible_timer = Timer.projectiles_hit_player_invincible_timer
                            player.is_invincible = True

                            wand.invincible_timer = Timer.projectiles_hit_wand_invincible_timer
                            wand.is_invincible = True

                            player.hurt_overlay_alpha = 92

                            shake_timer[0] = 20
                            pos = list(projectile.rect.center)
                            fx.create_impacts(pos)
                            fx.create_floating_particles(pos)
                            projectile.kill()
                            break

def all_enemies_touch_player(player: pygame.sprite.Sprite, wand, all_enemies_group, dt):
    Timer.enemies_touch_player_invincible_timer += dt
    Timer.enemies_touch_wand_invincible_timer += dt

    if not player.is_invincible and not player.has_survived:
        hits = pygame.sprite.spritecollide(player, all_enemies_group, False, collide_rect_then_mask)

        for enemy in hits:
            if player.current_shield != 0:
                player.current_shield -= 1
                player.shield_timer = pygame.time.get_ticks()
            else:
                player.current_hp -= 1
            if player.current_hp <= 0:
                player.kill()
                wand.kill()
            player.invincible_timer = Timer.enemies_touch_player_invincible_timer
            player.is_invincible = True

            wand.invincible_timer = Timer.enemies_touch_wand_invincible_timer
            wand.is_invincible = True

            player.hurt_overlay_alpha = 92

            # If touched by an enemy, break so that player wouldn't take
            # another damage if there are more than 2 enemies colliding
            # with player
            break

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
                    bullet.pierced_enemy_counter += 1
                
                if bullet.pierced_enemy_counter >= bullet.pierce_number:
                    bullet.kill()

def player_bullet_hit_ground_enemies(player_bullet_group):
    for bullet in player_bullet_group.sprites():
        for enemy in bullet.enemies_hit:
            if isinstance(enemy, (Tank, Light)):
                pos = list(bullet.rect.center)

                if not bullet.enemies_hit[enemy]:
                    fx.create_falling_particles(enemy, pos)
                    bullet.enemies_hit[enemy] = True
                    bullet.pierced_enemy_counter += 1
                
                if bullet.pierced_enemy_counter >= bullet.pierce_number:
                    bullet.kill()