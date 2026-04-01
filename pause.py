import pygame
from configs import display, DISPLAY_WIDTH, DISPLAY_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from font_system import FontSystem as fs

class Pause:
    continue_text_surf = fs.render_outlined("Continue", (255,255,255), (0,0,0), 2, fs.skill_name_font)
    continue_text_pos = [30, 420]
    continue_text_rect = continue_text_surf.get_rect(topleft=(continue_text_pos[0], continue_text_pos[1]))

    retry_text_surf = fs.render_outlined("Retry", (255,255,255), (0,0,0), 2, fs.skill_name_font)
    retry_text_pos = [30, 470]
    retry_text_rect = retry_text_surf.get_rect(topleft=(retry_text_pos[0], retry_text_pos[1]))

    back_text_surf = fs.render_outlined("Back to Main Menu", (255,255,255), (0,0,0), 2, fs.skill_name_font)
    back_text_pos = [30, 520]
    back_text_rect = back_text_surf.get_rect(topleft=(back_text_pos[0], back_text_pos[1]))

def show_pause_options(events, is_paused):
    mx, my = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH), (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT)

    for evt in events:
        if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
            if Pause.continue_text_rect.collidepoint(mx, my):
                is_paused[0] = not is_paused[0]
            elif Pause.retry_text_rect.collidepoint(mx, my):
                return False
            elif Pause.back_text_rect.collidepoint(mx, my):
                return True

    # This is responsible for the text surfaces movement since
    # they move x when mouse hovers over them
    # Move right if it is being hovered over else go back to normal position
    Pause.continue_text_pos[0] = min(50, Pause.continue_text_pos[0]+1) if Pause.continue_text_rect.collidepoint(mx, my) else max(30, Pause.continue_text_pos[0]-1)

    Pause.retry_text_pos[0] = min(50, Pause.retry_text_pos[0]+1) if Pause.retry_text_rect.collidepoint(mx, my) else max(30, Pause.retry_text_pos[0]-1)

    Pause.back_text_pos[0] = min(50, Pause.back_text_pos[0]+1) if Pause.back_text_rect.collidepoint(mx, my) else max(30, Pause.back_text_pos[0]-1)

    display.blit(Pause.continue_text_surf, (Pause.continue_text_pos[0], Pause.continue_text_pos[1]))
    display.blit(Pause.retry_text_surf, (Pause.retry_text_pos[0], Pause.retry_text_pos[1]))
    display.blit(Pause.back_text_surf, (Pause.back_text_pos[0], Pause.back_text_pos[1]))