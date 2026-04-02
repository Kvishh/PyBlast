import pygame

import sys
import effects_sytem as fx
from font_system import FontSystem as fs
from configs import *
from state import State
from game import Gameplay
from player import Player
from wand import Wand
from game_map import tiles_group, draw_background, create_tiles, draw_tiles, draw_behind_long_rocks, draw_front_long_rocks

class Menu(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        self.play_surf = fs.render_outlined("Play", (255,255,255), (0,0,0), 2, fs.menu_font)
        self.play_pos = [30, 360]
        self.play_rect = self.play_surf.get_rect(topleft=(self.play_pos[0] ,self.play_pos[1]))

        self.instructions_surf = fs.render_outlined("Instructions", (255,255,255), (0,0,0), 2, fs.menu_font)
        self.instructions_pos = [30, 410]
        self.instructions_rect = self.instructions_surf.get_rect(topleft=(self.instructions_pos[0] ,self.instructions_pos[1]))

        self.credits_surf = fs.render_outlined("Credits", (255,255,255), (0,0,0), 2, fs.menu_font)
        self.credits_pos = [30, 460]
        self.credits_rect = self.credits_surf.get_rect(topleft=(self.credits_pos[0], self.credits_pos[1]))

        self.quit_surf = fs.render_outlined("Quit", (255,255,255), (0,0,0), 2, fs.menu_font)
        self.quit_pos = [30, 510]
        self.quit_rect = self.quit_surf.get_rect(topleft=(self.quit_pos[0], self.quit_pos[1]))

        self.back_surf = fs.render_outlined("Back", (255,255,255), (0,0,0), 2, fs.menu_font)
        self.back_pos = [30, 20]
        self.back_rect = self.back_surf.get_rect(topleft=(self.back_pos[0], self.back_pos[1]))

        self.goal_surf = fs.render_outlined("Goal: Survive for 10 minutes. Defeat enemies to obtain upgrades.", (255,255,255), (0,0,0), 2, fs.skill_name_font)
        self.goal_pos = [50, 90]
        self.goal_rect = self.goal_surf.get_rect(topleft=(self.goal_pos[0], self.goal_pos[1]))

        self.abilities1_surf = fs.render_outlined("Abilities: Player dashes left or right depending where the cursor is.", (255,255,255), (0,0,0), 2, fs.skill_name_font)
        self.abilities1_pos = [50, 170]
        self.abilities1_rect = self.abilities1_surf.get_rect(topleft=(self.abilities1_pos[0], self.abilities1_pos[1]))

        self.abilities1_5_surf = fs.render_outlined("Player can't take any damage mid dash.", (255,255,255), (0,0,0), 2, fs.skill_name_font)
        self.abilities1_5_pos = [173, 220]
        self.abilities1_5_rect = self.abilities1_5_surf.get_rect(topleft=(self.abilities1_5_pos[0], self.abilities1_5_pos[1]))

        self.abilities2_surf = fs.render_outlined("Movement slows down when enemies' projectiles are\nnear player.", (255,255,255), (0,0,0), 2, fs.skill_name_font)
        self.abilities2_pos = [173, 270]
        self.abilities2_rect = self.abilities2_surf.get_rect(topleft=(self.abilities2_pos[0], self.abilities2_pos[1]))

        self.controls_surf = fs.render_outlined("Controls", (255,255,255), (0,0,0), 2, fs.font_timer)
        self.controls_pos = [(DISPLAY_WIDTH//2) - (self.controls_surf.get_rect().w//2), 370] # new 370
        self.controls_rect = self.controls_surf.get_rect(topleft=(self.controls_pos[0], self.controls_pos[1]))

        self.keys_surf = fs.render_outlined("LEFT CLICK - SHOOT | A/D - LEFT/RIGHT | SPACE - JUMP |", (255,255,255), (0,0,0), 2, fs.skill_name_font)
        self.keys_pos = [(DISPLAY_WIDTH//2) - self.keys_surf.get_rect().w//2, 440] # new 440
        self.keys_rect = self.keys_surf.get_rect(topleft=(self.keys_pos[0], self.keys_pos[1]))

        self.keys2_surf = fs.render_outlined("LEFT SHIFT - DASH | ESC - PAUSE", (255,255,255), (0,0,0), 2, fs.skill_name_font)
        self.keys2_pos = [(DISPLAY_WIDTH//2) - self.keys2_surf.get_rect().w//2, 490] # new 490
        self.keys2_rect = self.keys2_surf.get_rect(topleft=(self.keys2_pos[0], self.keys2_pos[1]))


        # For background ------------------------------------------------------------------------------------------------ #
        # Player --------------------------------------------------------------------------------------------------
        self.player = Player((WINDOW_WIDTH // 2) - PLAYER_WIDTH, 365)

        # Wand-----------------------------------------------------------------------------------------------------
        self.wand = Wand(self.player.rect.centerx, self.player.rect.centery)

        # Black Overlay -------------------------------------------------------------------------------------------
        self.dark_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.dark_overlay.fill((150,150,150,100)) # this is darker than the one in Gameplay

        # Scrolling (Camera effect)-------------------------------------------------------------------------------
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]

        # Function for creating tile-------------------------------------------------------------------------------
        # This checks if tiles_group.sprites() is empty, if it is empty call the function
        if not tiles_group.sprites(): create_tiles()

        # Blur destination surface --------------------------------------------------------------------------------
        self.blur_dest_surf = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.dark_blur_background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.dark_blur_background.fill((120,120,120,100))


    def update(self):
        self.new_state = False
        self.instruction_state = False

        main_menu_state = [True]

        running = True
        while running:
            events = pygame.event.get()
            for evt in events:
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evt.type == pygame.KEYDOWN:
                    if evt.key == pygame.K_RIGHT:
                        self.true_scroll[0] += 100
            # Checks the buttons that are clicked and perform the actions the buttons
            # are supposed to do
            mx, my = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH), (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT)
            if not self.instruction_state:
                self.check_buttons(events, (mx, my), main_menu_state)

            # This is for stopping this loop, used when transitioning to new state
            if self.new_state: break

            # DEFAULT
            dt = clock.tick(FPS) / 1000
            display.fill((42, 59, 95))
            self.dark_overlay.fill((150,150,150,100))

            # DEFAULT - Changing the scroll (camera) value
            self.true_scroll[0] += ((WINDOW_WIDTH // 2) - PLAYER_WIDTH - self.true_scroll[0] - (DISPLAY_WIDTH//2 - PLAYER_WIDTH//2))/20
            self.true_scroll[1] += (365 - self.true_scroll[1] - (DISPLAY_HEIGHT//2 - PLAYER_HEIGHT//2))/20

            dist = pygame.Vector2((WINDOW_WIDTH // 2) - PLAYER_WIDTH - self.true_scroll[0], 365 - self.true_scroll[1]).distance_to((mx, my))

            ax = dist if mx > DISPLAY_WIDTH // 2 else -dist
            ay = dist if  my > DISPLAY_HEIGHT // 2 else -dist

            self.true_scroll[0] += (ax * .004)
            self.true_scroll[1] += (ay * .004)

            if self.true_scroll[0] < 0:
                self.true_scroll[0] = 0
            elif self.true_scroll[0] > 1300-DISPLAY_WIDTH:
                self.true_scroll[0] = 1300-DISPLAY_WIDTH 

            if self.true_scroll[1] < 0:
                self.true_scroll[1] = 0
            elif self.true_scroll[1] > 800-DISPLAY_HEIGHT:
                self.true_scroll[1] = 800-DISPLAY_HEIGHT

            # DEFAULT - Actual values used in scrolling (camera)
            self.scroll = self.true_scroll.copy()
            self.scroll[0] = int(self.true_scroll[0])
            self.scroll[1] = int(self.true_scroll[1])

            # DEFAULT
            draw_background(self.scroll)
            draw_behind_long_rocks(self.scroll)
            draw_tiles(self.scroll, 200, dt)
            draw_front_long_rocks(self.scroll)

            # Creating background particles
            fx.create_background_particles()

            # Update and render of both player and wand
            self.player.update(pygame.key.get_pressed(), dt, self.dark_overlay, self.scroll, self.wand, alive=True)
            self.wand.update(self.player, self.scroll, self.player.rect.centerx, self.player.rect.centery, dt)
            self.wand.render(self.scroll)
            self.player.render(self.scroll)

            # Drawing background particles
            fx.draw_background_particles(self.dark_overlay, self.scroll, dt)
            # For dark overlay
            display.blit(self.dark_overlay, (0,0), special_flags=pygame.BLEND_RGB_MULT)


            # If player is in main menu and not in instruction state, draw buttons
            if main_menu_state[0] and not self.instruction_state:
                # Drawing of buttons
                self.draw_buttons()

            # If player is not in not main menu and in instruction state
            elif not main_menu_state[0] and self.instruction_state:
                # Lines responsible for the blurred background
                pygame.transform.box_blur(display, 5, dest_surface=self.blur_dest_surf)
                display.blit(self.blur_dest_surf)

                # Dark overlay 
                display.blit(self.dark_blur_background, (0,0), special_flags=pygame.BLEND_RGB_MULT)

                display.blit(self.goal_surf, self.goal_rect)
                display.blit(self.abilities1_surf, self.abilities1_rect)
                display.blit(self.abilities1_5_surf, self.abilities1_5_rect)
                display.blit(self.abilities2_surf, self.abilities2_rect)

                display.blit(self.controls_surf, self.controls_rect)

                display.blit(self.keys_surf, self.keys_rect)
                display.blit(self.keys2_surf, self.keys2_rect)

                self.show_back_button(events, (mx, my), main_menu_state)

            # last methods to be called
            window.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
            pygame.display.flip()
        
    def check_buttons(self, events, mouse_pos, main_menu_state):
        mx, my = mouse_pos[0], mouse_pos[1]

        for evt in events:
            if evt.type == pygame.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    if self.play_rect.collidepoint(mx, my):
                        self.state_manager.state_stack.append(Gameplay(self.state_manager))
                        print(len(self.state_manager.state_stack))
                        self.new_state = True
                    elif self.instructions_rect.collidepoint(mx, my):
                        self.instruction_state = True
                        main_menu_state[0] = False
                    elif self.credits_rect.collidepoint(mx, my):
                        print("credits")
                    elif self.quit_rect.collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()

        self.play_pos[0] = min(50, self.play_pos[0]+2) if self.play_rect.collidepoint(mx, my) else max(30, self.play_pos[0]-2)
        self.instructions_pos[0] = min(50, self.instructions_pos[0]+2) if self.instructions_rect.collidepoint(mx, my) else max(30, self.instructions_pos[0]-2)
        self.credits_pos[0] = min(50, self.credits_pos[0]+2) if self.credits_rect.collidepoint(mx, my) else max(30, self.credits_pos[0]-2)
        self.quit_pos[0] = min(50, self.quit_pos[0]+2) if self.quit_rect.collidepoint(mx, my) else max(30, self.quit_pos[0]-2)

    def draw_buttons(self):
        display.blit(self.play_surf, (self.play_pos[0], self.play_pos[1]))
        display.blit(self.instructions_surf, (self.instructions_pos[0], self.instructions_pos[1]))
        display.blit(self.credits_surf, (self.credits_pos[0], self.credits_pos[1]))
        display.blit(self.quit_surf, (self.quit_pos[0], self.quit_pos[1]))

    def show_back_button(self, events, mouse_pos, main_menu_state):
        mx, my = mouse_pos[0], mouse_pos[1]

        for evt in events:
            if evt.type == pygame.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    if self.back_rect.collidepoint(mx, my):
                        self.instruction_state = False
                        main_menu_state[0] = True

        self.back_pos[0] = min(40, self.back_pos[0]+2) if self.back_rect.collidepoint(mx, my) else max(30, self.back_pos[0]-2)

        display.blit(self.back_surf, (self.back_pos[0], self.back_pos[1]))
