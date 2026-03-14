import pygame, math, random
from configs import *
from game_map import tiles, tiles_blocks
from images import BulletImage

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, mouse_target_x, mouse_target_y):
        super().__init__()
        self.image = BulletImage.bullet_image_scaled
        self.rect = self.image.get_rect(center=(x, y+10))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 450
        self.direction = direction
        self.pos = pygame.Vector2(x, y+4)
        self._mouse_target_x = mouse_target_x
        self._mouse_target_y = mouse_target_y

        self.dy = self._mouse_target_y - self.pos.y
        self.dx = self._mouse_target_x - self.pos.x
        self._angle = math.atan2(self.dy, self.dx)
        self._x_vel = math.cos(self._angle)*self.speed
        self._y_vel = math.sin(self._angle)*self.speed

        self.pos += pygame.Vector2(17, 0).rotate(math.degrees(self._angle))

        self.particles = []
    
    def update(self, dt, scroll):
        ########## TRAIL PARTICLE ##########
        for particle in self.particles:
            particle[0][0] -= 1
            particle[0][1] += particle[1]
        particle = [list(self.rect.midleft), random.uniform(-2, 2), pygame.Color(random.randrange(204, 251), 255, 0)]
        self.particles.append(particle)
        if len(self.particles) > 20:
            self.particles.pop(0)
        ########## TRAIL PARTICLE ##########
        self._draw_particles(scroll)

        if self.rect.x > WINDOW_WIDTH:
            self.kill()
        elif self.rect.x < 0:
            self.kill()
        
        if self.direction > 0:
            self.speed = self.speed
        elif self.direction < 0:
            self.speed = -400

        self._kill_if_tile_collision()

        self._move(dt)

    def _move(self, dt):
        self.pos.x += self._x_vel * dt
        self.pos.y += self._y_vel * dt
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

    def _draw_particles(self, scroll):
        for i, particle in enumerate(self.particles):
            pygame.draw.circle(display, particle[2], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), (i//3+2))

    def _kill_if_tile_collision(self):
        tile_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

        bullet_tile_loc = (int(self.rect.x // TILE_SIZE), int(self.rect.y // TILE_SIZE))

        for offset in tile_offsets:
            check_loc = str(bullet_tile_loc[0] + offset[0]) + ";" + str(bullet_tile_loc[1] + offset[1])
            if check_loc in tiles_blocks:
                if tiles_blocks[check_loc].rect.colliderect(self.rect):
                    self.kill()