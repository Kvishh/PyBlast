import pygame, math, random
from configs import *
from game_map import tiles, tiles_blocks
from images import BulletImage

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, pierce_number, bounce_number, bullet_number, direction, skill_activated, mouse_target_x, mouse_target_y):
        super().__init__()
        self.image = BulletImage.bullet_image_scaled if not skill_activated else BulletImage.bullet_image_doubled_scaled
        self.rect = self.image.get_rect(center=(x, y+10))
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction
        self.pos = pygame.Vector2(x, y+4)
        self._mouse_target_x = mouse_target_x
        self._mouse_target_y = mouse_target_y

        self.speed = speed # 400 start, 650 max
        self.pierce_number = pierce_number
        self.bounce_number = bounce_number
        self.bullet_number = bullet_number

        self.enemies_hit = {}

        self.dy = self._mouse_target_y - self.pos.y
        self.dx = self._mouse_target_x - self.pos.x
        self._angle = math.atan2(self.dy, self.dx)
        self._x_vel = math.cos(self._angle)*self.speed
        self._y_vel = math.sin(self._angle)*self.speed

        self.pos += pygame.Vector2(17, 0).rotate(math.degrees(self._angle))

        self.particles = []
    
    def update(self, dt, scroll):
        self.create_trail_particle()
        self._draw_particles(scroll)

        if self.rect.x > WINDOW_WIDTH:
            self.kill()
        elif self.rect.x < 0:
            self.kill()
        
        if self.direction > 0:
            self.speed = self.speed
        elif self.direction < 0:
            self.speed = -1*self.speed

        self._move(dt)

    def _move(self, dt):
        self.pos.x += self._x_vel * dt
        self.pos.y += self._y_vel * dt
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

    def create_trail_particle(self):
        if len(self.particles) < 20:
            # location, velocity, radius, color
            self.particles.append([list(self.rect.center),
                                   [random.randint(-1, 1), random.uniform(-2.5, 2.5)],
                                   random.randrange(7, 11),
                                   pygame.Color(random.randrange(204, 251), 255, 0)])

    def _draw_particles(self, scroll):
        if self.particles:
            self.particles = [p for p in self.particles if p[2] > 0]

            for particle in self.particles:
                particle[0][0] -= particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= .3

                pygame.draw.circle(display, (60, 74, 0), (particle[0][0]-scroll[0]+4, particle[0][1]-scroll[1]+4), (particle[2]))
                pygame.draw.circle(display, particle[3], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), (particle[2]))