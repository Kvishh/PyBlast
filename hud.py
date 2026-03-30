import pygame
from configs import *
from images import HUDImage
from font_system import FontSystem as fs

class HUD:
    def __init__(self, player):
        self.player = player
        self.heart = HUDImage.heart_image_scaled
        self.empty_heart = HUDImage.empty_heart_image_scaled
        self.shield = HUDImage.shield_image_scaled
        self.dash = HUDImage.dash_image_scaled

        self.level = 1
        self.level_bar = pygame.Rect(10, 10, 980, 20) # Rect: 10, 10, 980, 20-left,top,width,height
        self.current_xp_width = 0

        # "FPS: " text cache for fps
        self.FPS_text = fs.render_outlined(("FPS: "), (255,255,255), (0,0,0), 2, fs.font_fps)
        self.cached_fps = {}

        # ":" colon cache for timer
        self.colon_text_surf = fs.render_outlined(":", (255,255,255), (0,0,0), 2, fs.font_timer)

        # Minutes cache dict
        # The key will be string and value will be the actual surface
        self.minutes_timer_caches = {}
        for i in range(0, 11):
            # If i is less than 10, then the string will be "0{i}" where i is 0-9 (inclusive)
            if i < 10:
                self.minutes_timer_caches[f"0{i}"] = fs.render_outlined(f"0{i}", (255,255,255), (0,0,0), 2, fs.font_timer)
            # If i is greater than 10, then the string will be "i" where i is 10 (inclusive)
            else:
                self.minutes_timer_caches[str(i)] = fs.render_outlined(str(i), (255,255,255), (0,0,0), 2, fs.font_timer)

        # Seconds cache dict
        # The key will be string and value will be the actual surface
        self.seconds_timer_caches = {}
        for i in range(0, 60):
            # If i is less than 10, then the string will be "0{i}" where i is 0-9 (inclusive)
            if i < 10:
                self.seconds_timer_caches[f"0{i}"] = fs.render_outlined(f"0{i}", (255,255,255), (0,0,0), 2, fs.font_timer)
            # If i is greater than 10, then the string will be "i" where i is 10-59 (inclusive)
            else:
                self.seconds_timer_caches[str(i)] = fs.render_outlined(str(i), (255,255,255), (0,0,0), 2, fs.font_timer)

        # "Survive!" text cache
        self.survive_text = fs.render_outlined("Survive!", (235, 0, 0), (0,0,0), 2, fs.font)

        # This is for "lvl" text, the level number is not included
        self.lvl_text = fs.render_outlined("Lvl ", (255,255,255), (0,0,0), 2, fs.font_level)

    
    def update(self, player, timer, xp_increment, level_up_state, last_frame):
        self._blit_heart()
        self._blit_shield()
        self._update_and_draw_dash(player)
        self.blit_FPS()
        self.blit_timer(timer)
        self._blit_level_bar()
        self.update_level_bar(xp_increment, level_up_state, last_frame)

    def update_level_bar(self, xp_increment, level_up_state, last_frame):
        self.current_xp_width += xp_increment[0]
        if self.current_xp_width >= 980:
            # The width before addition
            old_xp_width = self.current_xp_width - xp_increment[0]
            # The difference in order to get the amount that will be subtracted to the increment
            diff = 980 - old_xp_width
            # The surplus added after leveling up
            xp_increment[0] = xp_increment[0] - diff
            
            self.current_xp_width = 980 - (980 - xp_increment[0])
            self.level += 1

            # Calling this again so that the level bar (the green bar that represents xp player has)
            # is updated immediately after increasing it. This makes the last frame has the updated 
            # level to its next level and the green bar to its new width
            
            # Otherwise, the last frame will be left to its old green bar and level despite it being already
            # on next level. Only then will it be updated after the player has chosen an upgrade
            self._blit_level_bar()
            last_frame.append(display.copy())
            level_up_state[0] = True
        elif self.current_xp_width <= 0:
            self.current_xp_width = 0

    def _blit_level_bar(self):
        # Black background
        pygame.draw.rect(display, (0,0,0), self.level_bar)
        
        # The green level bar
        pygame.draw.rect(display, (0,255,0), (self.level_bar.left, self.level_bar.top, self.current_xp_width, self.level_bar.height))

        # Level text rendering
        # This is for actual level number
        text = fs.render_outlined(f"{str(self.level)}", (255,255,255), (0,0,0), 2, fs.font_level)
        display.blit(text, ((DISPLAY_WIDTH//2)+10,7))
        
        # This is for "lvl" text, not the level number
        display.blit(self.lvl_text, ((DISPLAY_WIDTH//2)-10,7))

        # White outline
        pygame.draw.rect(display, (255,255,255), self.level_bar, 2)

    def _update_and_draw_dash(self, player):
        if player.dash_num == 0: display.blit(self.dash, (15, 140))

    def _blit_heart(self):
        empty_num = 0
        if self.player.current_hp < self.player.max_hp :
            empty_num = self.player.max_hp - self.player.current_hp

        for i in range(self.player.current_hp):
            display.blit(self.heart, (10+i*(EMPTY_HEART_IMAGE_WIDTH + 5), 40))
        
        if empty_num != 0:
            for i in range(self.player.current_hp, self.player.current_hp+empty_num):
                display.blit(self.empty_heart, (10+(i*(EMPTY_HEART_IMAGE_WIDTH + 5)), 40))
    
    def _blit_shield(self):
        for i in range(self.player.current_shield):
            display.blit(self.shield, (10+(i*(SHIELD_IMAGE_WIDTH + 5)), 85))
    
    def blit_FPS(self):
        fps_value = f"{clock.get_fps():.0f}"
        
        # For caching. If fps value not in cached dict yet, only then create new text surface (render_outlline method
        # returns new surface), else don't create new text surface since it has been previously created and use that
        if not fps_value in self.cached_fps:
            self.cached_fps[fps_value] = fs.render_outlined(fps_value, (255,255,255), (0,0,0), 2, fs.font_fps)

        display.blit(self.FPS_text, (DISPLAY_WIDTH-75,100))
        display.blit(self.cached_fps[fps_value], (DISPLAY_WIDTH-37,100))

    def blit_timer(self, timer):
        minute_text = timer[0]
        second_text = timer[1]

        # Blitting of caches timer text
        display.blit(self.minutes_timer_caches[minute_text], (DISPLAY_WIDTH-110,25))
        display.blit(self.colon_text_surf, (DISPLAY_WIDTH-66,25))
        display.blit(self.seconds_timer_caches[second_text], (DISPLAY_WIDTH-55,25))

        # The "Survive!" text is cached
        display.blit(self.survive_text, (DISPLAY_WIDTH-85,70))
    