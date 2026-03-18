import pygame, math, random
from configs import *
from game_map import tiles, tile_map
from images import EnemyBulletImage, SpecterEnemyBulletImage

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, target_x, target_y):
        super().__init__()
        self.image = EnemyBulletImage.enemy_bullet_image_scaled
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 450
        self.direction = direction
        self.pos = pygame.Vector2(x, y)
        self.target_x = target_x
        self.target_y = target_y

        self.dy = self.target_y - self.pos.y
        self.dx = self.target_x - self.pos.x
        self._angle = math.atan2(self.dy, self.dx)
        self._x_vel = math.cos(self._angle)*self.speed
        self._y_vel = math.sin(self._angle)*self.speed

        self.particles = []

        self.line_width = 3
        self.end_p = self.cast_line()
    
    def update(self, dt, scroll):
        self.create_trail_particle()
        self._draw_particles(scroll)

        self.draw_line(scroll)

        if self.rect.x > WINDOW_WIDTH:
            self.kill()
        elif self.rect.x < 0:
            self.kill()

        if self.rect.y > WINDOW_HEIGHT:
            self.kill()
        elif self.rect.y < 0:
            self.kill()
        
        if self.direction > 0:
            self.speed = self.speed
        elif self.direction < 0:
            self.speed = -400

        self._move(dt)

    def _move(self, dt):
        self.pos.x += self._x_vel * dt
        self.pos.y += self._y_vel * dt
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

    def _draw_particles(self, scroll):
        if self.particles:
            self.particles = [p for p in self.particles if p[2] > 0]

            for particle in self.particles:
                particle[0][0] -= particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= .4

                pygame.draw.circle(display, (48, 18, 56), (particle[0][0]-scroll[0]+4, particle[0][1]-scroll[1]+4), (particle[2]))
                pygame.draw.circle(display, particle[3], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), (particle[2]))

    def create_trail_particle(self):
        if len(self.particles) < 20:
            # location, velocity, radius, color
            self.particles.append([list(self.rect.center),
                                   [random.randint(-1, 1), random.uniform(-2.5, 2.5)],
                                   random.randrange(7, 11),
                                   pygame.Color(random.randrange(147, 206), 43, 207)])

    def draw_line(self, scroll):
        start = (self.rect.centerx, self.rect.centery)

        pygame.draw.line(display, (255,0,0), (start[0]-scroll[0], start[1]-scroll[1 ]), (self.end_p[0]-scroll[0], self.end_p[1]-scroll[1]), int(self.line_width))

    def cast_line(self):
        start = (self.rect.centerx, self.rect.centery)
        end = (self.target_x, self.target_y)
        
        dx, dy = end[0] - start[0], end[1] - start[1]
        dist = math.hypot(dx, dy)

        if dist == 0: return start

        dx /= dist
        dy /= dist

        x, y = start[0], start[1]

        max_radius = math.hypot(window.width, window.height)

        for i in range(int(max_radius)):
            x += dx
            y += dy

            tile_x, tile_y = int(x // TILE_SIZE), int(y // TILE_SIZE)

            if tile_y < 0 or tile_y >= len(tile_map) or tile_x < 0 or tile_x >= len(tile_map[0]):
                return (x, y)

            if tile_map[tile_y][tile_x] == 1:
                return (x, y)

        final_x = start[0] + dx * max_radius
        final_y = start[1] + dy * max_radius

        end = (final_x, final_y)
            
        return end

class SpecterEnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, target_x, target_y):
        super().__init__()
        self.image = SpecterEnemyBulletImage.specter_enemy_bullet_image_scaled
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 450
        self.direction = direction
        self.pos = pygame.Vector2(x, y)
        self.target_x = target_x
        self.target_y = target_y

        self.dy = self.target_y - self.pos.y
        self.dx = self.target_x - self.pos.x
        self._angle = math.atan2(self.dy, self.dx)
        self._x_vel = math.cos(self._angle)*self.speed
        self._y_vel = math.sin(self._angle)*self.speed

        self.particles = []
        self.opacity = 210
        self.turn = 1

        self.line_width = 3
        self.end_p = self.cast_line()
    
    def update(self, dt, scroll):
        self.create_trail_particle()
        self._draw_particles(scroll)

        self.draw_line(scroll)

        if self.turn == 1:
            if self.opacity < 220:
                self.opacity += 3
            else:
                self.opacity += 0
                self.turn = -1
        elif self.turn == -1:
            if self.opacity > 40:
                print
                self.opacity -= 3
            else:
                self.opacity += 0
                self.turn = 1
        self.image.set_alpha(self.opacity)

        if self.rect.x > WINDOW_WIDTH:
            self.kill()
        elif self.rect.x < 0:
            self.kill()

        if self.rect.y > WINDOW_HEIGHT:
            self.kill()
        elif self.rect.y < 0:
            self.kill()
        
        if self.direction > 0:
            self.speed = self.speed
        elif self.direction < 0:
            self.speed = -400

        self._move(dt)

    def draw_line(self, scroll):
        start = (self.rect.centerx, self.rect.centery)

        pygame.draw.line(display, (255,0,0), (start[0]-scroll[0], start[1]-scroll[1 ]), (self.end_p[0]-scroll[0], self.end_p[1]-scroll[1]), int(self.line_width))

    def cast_line(self):
        start = (self.rect.centerx, self.rect.centery)
        end = (self.target_x, self.target_y)
        
        dx, dy = end[0] - start[0], end[1] - start[1]
        dist = math.hypot(dx, dy)

        if dist == 0: return start

        dx /= dist
        dy /= dist

        max_radius = math.hypot(window.width, window.height)

        final_x = start[0] + dx * max_radius
        final_y = start[1] + dy * max_radius

        end = (final_x, final_y)
            
        return end

    def _move(self, dt):
        self.pos.x += self._x_vel * dt
        self.pos.y += self._y_vel * dt
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

    def _draw_particles(self, scroll):
        if self.particles:
            self.particles = [p for p in self.particles if p[2] > 0]

            for particle in self.particles:
                particle[0][0] -= particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= .4

                radius = particle[2]
                circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                shadow = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

                pygame.draw.circle(shadow, (48, 18, 56, self.opacity), (radius, radius), radius)

                pygame.draw.circle(circle, (particle[3][0], particle[3][1], particle[3][2], self.opacity), (radius, radius), radius)

                x = particle[0][0] - radius
                y = particle[0][1] - radius

                display.blit(shadow, (x-scroll[0]+3, y-scroll[1]+3))
                display.blit(circle, (x-scroll[0], y-scroll[1]))

    def create_trail_particle(self):
        if len(self.particles) < 20:
            # location, velocity, radius, color
            self.particles.append([list(self.rect.center),
                                   [random.randint(-1, 1), random.uniform(-2.5, 2.5)],
                                   random.randrange(7, 11),
                                   pygame.Color(random.randrange(147, 206), 43, 207)])