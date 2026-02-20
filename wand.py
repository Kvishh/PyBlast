import pygame, math
from configs import *

class Wand(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load("assets/images/player_wand.png").convert_alpha(), -90) # positive will rotate it counterclockwise
        self.rect = self.image.get_rect(center=(x, y))
        self.orig_image = self.image
        self.pivot_point = self.rect.centerx/2, self.rect.centery/2 # ORIGINAL!!!
        self.offset = pygame.math.Vector2(20, 0)
    
    def update(self, player, scroll, x, y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_x = mouse_pos[0] + scroll[0]
        mouse_pos_y = mouse_pos[1] + scroll[1]
        pl_x = x
        pl_y = y

        self.rect.center = player.rect.center

        dx = mouse_pos_x - pl_x
        dy = mouse_pos_y - pl_y

        angle_mouse = math.degrees(math.atan2(dy, dx))
        self._rotate_around_pivot(angle_mouse, x, y)

        # DON'T TOUCH ABOVE !!! THOSE THAT ARE COMMENTED


        # dx, dy = mouse_pos_x - player.rect.centerx, mouse_pos_y - player.rect.centery
        # angle = math.degrees(math.atan2(-dy, dx)) - 0 # CORRECTION ANGLE

        # self.image = pygame.transform.rotate(self.orig_image, angle)
        # self.rect = self.image.get_rect(center=(player.rect.centerx+50, player.rect.centery))


    def render(self, scroll):
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        # pygame.draw.rect(display, (255, 0, 0), (self.rect.x - scroll[0], self.rect.y - scroll[1], 50, 50), 2)

    def _rotate_around_pivot(self, angle, x, y):
        self.image = pygame.transform.rotate(self.orig_image, -angle) # ORIGNAL !!
        rotated_offset = self.offset.rotate(angle)

        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery) + rotated_offset) # ORIGNAL !! # RESPONSIBLE FOR CHANGING/SHIFTING THE PIVOT POINT OF ROTATION
        # self.rect = self.image.get_rect(center = (x, y) + rotated_offset) # ALSO CORRECT !! # RESPONSIBLE FOR CHANGING/SHIFTING THE PIVOT POINT OF ROTATION
        # self.rect.center = (x, y) + rotated_offset # add pos values to y to draw it more below # RESPONSIBLE FOR PLACEMENT OF THE IMAGE, COULD BE CENTER
        # OF PLAYER OR MORE TO THE RIGHT OF PLAYER