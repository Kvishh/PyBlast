import pygame
from configs import *
from player import *
from game_map import *
from player import *

pygame.init()
pygame.display.init()

player = Player(0, 0)

# bg_bottom = pygame.image.load("assets/images/bg_1.png").convert_alpha()

create_tiles()

def game_run():
    running = True
    while running:
        clock.tick(FPS)
        display.fill((56, 56, 56))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_tiles()
        
        player.update()
        player.render([0, 0])

        # display.blit(bg_bottom, (0, 0))

        # keys_hold = pygame.key.get_pressed()
        # if keys_hold[pygame.K_SPACE] and not player.jumping:
        #     player.y_velocity = -16
        #     player.jumping = True
        # elif keys_hold[pygame.K_d]:
        #     player.x_velocity = 5
        #     player.x_direction = 1
        # elif keys_hold[pygame.K_a]:
        #     player.x_velocity = -5
        #     player.x_direction = -1
        
        # last method to be called
        window.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    game_run()