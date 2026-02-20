import pygame
from configs import *
from player import *
from game_map import *
from player import *
from wand import *
from bullet import *
from customgroup import *

# Must calls
pygame.init()
pygame.display.init()

# game components
# Player----------------------------------------------
player = Player(0, 0)

# Wand------------------------------------------------
wand = Wand(player.rect.centerx, player.rect.centery)

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

def shoot_bullet(previous_time):
    mouse_hold = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if mouse_hold[0]:
        current_time = pygame.time.get_ticks()
        if current_time - previous_time[0] > SHOOTING_COOLDOWN:
            bullet = Bullet("assets/images/bullet.png", player.rect.centerx, player.rect.centery, scroll, player.x_direction, mouse_pos[0], mouse_pos[1])
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
        player.update(pygame.key.get_pressed(), dt)
        player.render(scroll)
        wand.update(player, scroll, player.rect.centerx, player.rect.centery)
        wand.render(scroll)

        # Checking of mouse hold and creation of bullet
        shoot_bullet(previous_time)

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