import pygame
from configs import *
from player import *
from game_map import *
from player import *

# Must calls
pygame.init()
pygame.display.init()

# game components
# Player----------------------------------------------
player = Player(0, 0)

# Scrolling (Camera effect)---------------------------
true_scroll = [0, 0]
scroll = [0, 0]

# Function for creating tile--------------------------
create_tiles()

# Function for creating background-------------------
load_bg_images()


def game_run():
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

        # For drawing tiles
        draw_tiles(scroll)
        
        player.update(pygame.key.get_pressed(), dt)
        player.render(scroll)

        # last methods to be called
        window.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.flip()



if __name__ == "__main__":
    game_run()