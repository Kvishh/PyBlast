import pygame, math
from configs import *
from images import WandImage

class Wand(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = WandImage.wand_image_rotated
        self.rect = self.image.get_rect(center=(x, y))
        self.orig_image = self.image
        self.pivot_point = self.rect.centerx/2, self.rect.centery/2
        self.offset = pygame.math.Vector2(20, 0)

        self.is_invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1.5

        self.is_hit_current_timer = 0
        self.blink_timer = 0
        self.blink_state = 0
    
    def update(self, player, scroll, x, y, dt):
        mouse_pos_x = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH) + scroll[0]
        mouse_pos_y = (pygame.mouse.get_pos()[1] * DISPLAY_WIDTH / WINDOW_WIDTH) + scroll[1]
        pl_x = x
        pl_y = y
        self.rect.center = player.rect.center
        dx = mouse_pos_x - pl_x
        dy = mouse_pos_y - pl_y
        angle_mouse = math.degrees(math.atan2(dy, dx))

        self._rotate_around_pivot(angle_mouse, x, y)
        self._switch_player_orientation(player, angle_mouse)

        self.player_is_hit(dt)

        if abs(player.dash_num) >= 45:
            self.image.set_alpha(0)

    def render(self, scroll):
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def player_is_hit(self, dt):
        self.is_hit_current_timer += dt

        if self.is_invincible:
            if self.is_hit_current_timer - self.invincible_timer > self.invincible_duration:
                self.is_invincible = False

            self.blink_timer += dt
            if self.blink_timer >= .1:
                self.blink_timer = 0
                self.blink_state = not self.blink_state

            if self.blink_state:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def _rotate_around_pivot(self, angle, x, y):
        self.image = pygame.transform.rotate(self.orig_image, -angle)
        rotated_offset = self.offset.rotate(angle)

        self.rect = self.image.get_rect(center = (self.rect.centerx+5, self.rect.centery+2) + rotated_offset)

    def _switch_player_orientation(self, player, angle):
        player.x_direction = -1 if angle > 90 or angle < -90 else 1
       