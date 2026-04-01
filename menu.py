import pygame

import sys
from configs import *
from state import State

class Menu(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)

    def update(self):
        running = True
        while running:
            events = pygame.event.get()
            for evt in events:
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = clock.tick(FPS) / 1000
            display.fill((42, 59, 95))
            
            # last methods to be called
            window.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
            pygame.display.flip()
        
        self.state_manager.state_stack.pop()