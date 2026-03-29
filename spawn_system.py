import pygame, random, math
from configs import *
from customgroup import CustomGroup, ShootCustomGroup
from light import Light
from tank import Tank
from flight import Flight
from soar import Soar
from shoot import Shoot
from burst import Burst
from specter import Specter

class Enemies:
    # Light enemy Group----------------------------------------------------------------------------------------
    light_enemy_group = CustomGroup()

    # Tank enemy Group-----------------------------------------------------------------------------------------
    tank_enemy_group = CustomGroup()

    # Flight enemy group---------------------------------------------------------------------------------------
    flight_enemy_group = CustomGroup()

    # Soar enemy group-----------------------------------------------------------------------------------------
    soar_enemy_group = CustomGroup()        

    # Shooting enemy group-------------------------------------------------------------------------------------
    shoot_enemy_group = ShootCustomGroup()

    # Burst enemy group----------------------------------------------------------------------------------------
    burst_enemy_group = ShootCustomGroup()

    # Specter enemy group--------------------------------------------------------------------------------------
    specter_enemy_group = ShootCustomGroup()


    # Enemy Bullet group---------------------------------------------------------------------------------------
    enemy_bullet_group = CustomGroup()

    # Specter Enemy Bullet group-------------------------------------------------------------------------------
    specter_enemy_bullet_group = CustomGroup()

    ### RELATED GROUPS --------------------------------------------------------------------------------------------------- ###
    # For walking enemies--------------------------------------------------------------------------------------
    all_ground_enemies = CustomGroup(light_enemy_group, tank_enemy_group)

    # For flying enemies---------------------------------------------------------------------------------------
    all_flying_enemies = CustomGroup(flight_enemy_group, soar_enemy_group, shoot_enemy_group, burst_enemy_group, specter_enemy_group)

    # Group for of all enemies that can damage player-----------------------------------------------------------
    all_enemies_group = pygame.sprite.Group(*all_ground_enemies, *all_flying_enemies)

    # Group for all enemies that can be detected as hit by player bullet----------------------------------------
    all_enemies_that_can_be_hit_by_playerbullet_group = pygame.sprite.Group(*all_ground_enemies, *flight_enemy_group, *soar_enemy_group, *shoot_enemy_group, *burst_enemy_group, *specter_enemy_group)


    # Set of all types of enemies-------------------------------------------------------------------------------
    enemies_types = ["Light", "Tank", "Flight", "Soar", "Shoot", "Burst", "Specter"]


def spawn_enemies(current_level, spawn_rect, spawn_session_num, set_of_alive_enemies, countdown_time):
    multiplier = 4 if spawn_session_num < 2 else 3

    if current_level <= 10:
        num_of_enemies_that_will_spawn = ((current_level * multiplier) // (len(set_of_alive_enemies) if len(set_of_alive_enemies) != 0 else 1)) // 2
    else:
        num_of_enemies_that_will_spawn = (current_level * multiplier) // (len(set_of_alive_enemies) if len(set_of_alive_enemies) != 0 else 1)

    for i in range(num_of_enemies_that_will_spawn):
        chance = random.random()

        match str(spawn_session_num):
            case "1": # Start at 9 min mark
                if chance < .3:
                    spawn_ground_enemies(spawn_rect, set_of_alive_enemies, "Tank") if current_level < 20 else spawn_ground_enemies(spawn_rect, set_of_alive_enemies, "Tank", multiply_hp=True)
                else:
                    spawn_ground_enemies(spawn_rect, set_of_alive_enemies, "Light") if current_level < 20 else spawn_ground_enemies(spawn_rect, set_of_alive_enemies, "Light", multiply_hp=True)
            case "2": # Start at 8 min mark
                if chance < .2:
                    spawn_ground_enemies(spawn_rect, set_of_alive_enemies, "Tank") if current_level < 20 else spawn_ground_enemies(spawn_rect, set_of_alive_enemies, "Tank", multiply_hp=True)
                else:
                    spawn_flying_enemies(set_of_alive_enemies, "Flight") if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, "Flight", multiply_hp=True)
            case "3": # Start at 7 min mark
                if chance < .4:
                    enemy_type = choose_enemy(["Flight", "Soar"])
                    spawn_flying_enemies(set_of_alive_enemies, enemy_type) if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, enemy_type, multiply_hp=True)
                else:
                    spawn_flying_enemies(set_of_alive_enemies, "Shoot") if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, "Shoot", multiply_hp=True)
            case "4": # Start at 6 min mark
                if chance < .4:
                    enemy_type = choose_enemy(["Shoot", "Soar", "Burst"])
                    spawn_flying_enemies(set_of_alive_enemies, enemy_type) if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, enemy_type, multiply_hp=True)
                else:
                    spawn_flying_enemies(set_of_alive_enemies, "Specter") if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, "Specter", multiply_hp=True)
            case "5": # Start at 5 min mark
                if chance < .2:
                    spawn_ground_enemies(spawn_rect, set_of_alive_enemies, "Tank") if current_level < 20 else spawn_ground_enemies(spawn_rect, set_of_alive_enemies, "Tank", multiply_hp=True)
                elif chance >= .2 and chance <= .4:
                    enemy_type = choose_enemy(["Soar", "Shoot", "Burst"])
                    spawn_flying_enemies(set_of_alive_enemies, enemy_type) if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, enemy_type, multiply_hp=True)
                else:
                    spawn_flying_enemies(set_of_alive_enemies, "Specter") if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, "Specter", multiply_hp=True)
            case "6": # Start at 4 min mark
                if chance <.2:
                    enemy_type = choose_enemy(["Light", "Tank"])
                    spawn_ground_enemies(spawn_rect, set_of_alive_enemies, enemy_type) if current_level < 20 else spawn_ground_enemies(spawn_rect, set_of_alive_enemies, enemy_type, multiply_hp=True)
                if chance > .2 and chance < .4:
                    enemy_type = choose_enemy(["Flight", "Soar", "Shoot", "Burst"])
                    spawn_flying_enemies(set_of_alive_enemies, enemy_type) if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, enemy_type, multiply_hp=True)
                else:
                    spawn_flying_enemies(set_of_alive_enemies, "Specter") if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, "Specter", multiply_hp=True)
            case "7": # Start at 3 min mark
                if chance <.4:
                    enemy_type = choose_enemy(["Flight", "Tank"])
                    if enemy_type == "Tank":
                        spawn_ground_enemies(spawn_rect, set_of_alive_enemies, enemy_type) if current_level < 20 else spawn_ground_enemies(spawn_rect, set_of_alive_enemies, enemy_type, multiply_hp=True)
                    else:
                        spawn_flying_enemies(set_of_alive_enemies, enemy_type) if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, enemy_type, multiply_hp=True)
                else:
                    spawn_flying_enemies(set_of_alive_enemies, "Specter") if current_level < 20 else spawn_flying_enemies(set_of_alive_enemies, "Specter", multiply_hp=True)

def choose_enemy(selected_type):
    enemy_type = random.choice(Enemies.enemies_types)
    while True:
        if enemy_type in selected_type:
            break
        enemy_type = random.choice(Enemies.enemies_types)
    return enemy_type

def spawn_ground_enemies(spawn_rect, set_of_alive_enemies, enemy_type, multiply_hp=False):
    x = random.randint(0, WINDOW_WIDTH-HEAVY_ENEMY_WIDTH)
    if enemy_type == "Tank":
        while True:
            x = random.randint(0, WINDOW_WIDTH-HEAVY_ENEMY_WIDTH)
            if x < spawn_rect.left or x > spawn_rect.right:
                break
        enemy = Tank(x, FLOOR, Enemies.tank_enemy_group, Enemies.all_ground_enemies, Enemies.all_enemies_that_can_be_hit_by_playerbullet_group, Enemies.all_enemies_group)
        if multiply_hp: enemy.hp *= 3
        set_of_alive_enemies.add(enemy)
    else:
        x = random.randint(0, WINDOW_WIDTH-HEAVY_ENEMY_WIDTH)
        while True:
            x = random.randint(0, WINDOW_WIDTH-HEAVY_ENEMY_WIDTH)
            if x < spawn_rect.left or x > spawn_rect.right:
                break
        enemy = Light(x, FLOOR, Enemies.light_enemy_group, Enemies.all_ground_enemies, Enemies.all_enemies_that_can_be_hit_by_playerbullet_group, Enemies.all_enemies_group)
        if multiply_hp: enemy.hp *= 3
        set_of_alive_enemies.add(enemy)

def spawn_flying_enemies(set_of_alive_enemies, enemy_type, multiply_hp=False):
    x = random.randint(0, WINDOW_WIDTH)
    match enemy_type:
        case "Flight":
            enemy = Flight(x, -10, Enemies.flight_enemy_group, Enemies.all_flying_enemies, Enemies. all_enemies_that_can_be_hit_by_playerbullet_group, Enemies.all_enemies_group)
            if multiply_hp: enemy.hp *= 3
            set_of_alive_enemies.add(enemy)
        case "Soar":
            enemy = Soar(x, -10, Enemies.soar_enemy_group, Enemies.all_flying_enemies, Enemies. all_enemies_that_can_be_hit_by_playerbullet_group, Enemies.all_enemies_group)
            if multiply_hp: enemy.hp *= 3
            set_of_alive_enemies.add(enemy)
        case "Shoot":
            enemy = Shoot(x, -10, Enemies.shoot_enemy_group, Enemies.all_flying_enemies, Enemies. all_enemies_that_can_be_hit_by_playerbullet_group, Enemies.all_enemies_group)
            if multiply_hp: enemy.hp *= 3
            set_of_alive_enemies.add(enemy)
        case "Burst":
            enemy = Burst(x, -10, Enemies.burst_enemy_group, Enemies.all_flying_enemies, Enemies. all_enemies_that_can_be_hit_by_playerbullet_group, Enemies.all_enemies_group)
            if multiply_hp: enemy.hp *= 3
            set_of_alive_enemies.add(enemy)
        case "Specter":
            enemy = Specter(x, -10, Enemies.specter_enemy_group, Enemies.all_flying_enemies, Enemies. all_enemies_that_can_be_hit_by_playerbullet_group, Enemies.all_enemies_group)
            if multiply_hp: enemy.hp *= 3
            set_of_alive_enemies.add(enemy)