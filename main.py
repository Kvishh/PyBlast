import pygame
from configs import *
from player import *
from game_map import *
from player import *
from wand import *
from bullet import *
from customgroup import *
from enemy import *

# Must calls
pygame.init()
pygame.display.init()

# game components
# Player----------------------------------------------
player = Player(0, 0)

# Wand------------------------------------------------
wand = Wand(player.rect.centerx, player.rect.centery)

# Enemy-----------------------------------------------
enemy = Enemy(0, 0)

# Bullets---------------------------------------------
bullet_group = CustomGroup()

# Scrolling (Camera effect)---------------------------
true_scroll = [0, 0]
scroll = [0, 0]

# Function for creating tile--------------------------
create_tiles()

# Function for creating background-------------------
load_bg_images()

# Function for loading background images-------------
load_long_rocks()

def shoot_bullet(previous_time, scroll, player_rect_centerx, player_rect_centery):
    mouse_hold = pygame.mouse.get_pressed()
    if mouse_hold[0]:
        current_time = pygame.time.get_ticks()
        if current_time - previous_time[0] > SHOOTING_COOLDOWN:

            mouse_x = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH) + scroll[0]
            mouse_y = (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT) + scroll[1]
            
            bullet = Bullet("assets/images/bullet.png", 
                            player_rect_centerx, 
                            player_rect_centery, 
                            player.x_direction, 
                            mouse_x,
                            mouse_y)
            bullet_group.add(bullet)
            previous_time[0] = current_time


def game_run():
    previous_time = [pygame.time.get_ticks()]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(FPS) / 1000
        display.fill((42, 59, 95))

        # Changing the scroll (camera) value
        true_scroll[0] += (player.rect.x - true_scroll[0] - (DISPLAY_WIDTH//2 - PLAYER_WIDTH//2))/20
        true_scroll[1] += (player.rect.y - true_scroll[1] - (DISPLAY_HEIGHT//2 - PLAYER_HEIGHT//2))/20

        if true_scroll[0] < 0:
            true_scroll[0] = 0
        elif true_scroll[0] > 1300-DISPLAY_WIDTH:
            true_scroll[0] = 1300-DISPLAY_WIDTH 

        if true_scroll[1] < 0:
            true_scroll[1] = 0
        elif true_scroll[1] > 800-DISPLAY_HEIGHT:
            true_scroll[1] = 800-DISPLAY_HEIGHT

        # Actual values used in scrolling (camera)
        scroll = true_scroll.copy()
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])

        # For drawing background
        draw_background(scroll)

        # Drawing behind platforms but in front of background
        draw_behind_long_rocks(scroll)

        # For drawing tiles
        draw_tiles(scroll)
        
        # Player and Wand update and draw methods
        wand.update(player, scroll, player.rect.centerx, player.rect.centery)
        wand.render(scroll)
        player.update(pygame.key.get_pressed(), dt)
        player.render(scroll)

        # Enemmy update and render
        enemy.update(dt, scroll, player)
        enemy.render(scroll)

        # Checking of mouse hold and creation of bullet
        shoot_bullet(previous_time, scroll, player.rect.centerx, player.rect.centery)

        # Drawing of bullets
        bullet_group.update(dt, scroll)
        bullet_group.draw(display, scroll)

        # Rendering of front objects (long rocks)
        draw_front_long_rocks(scroll)

        # last methods to be called
        window.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.flip()
    
    # Quit the window
    pygame.quit()


if __name__ == "__main__":
    game_run()