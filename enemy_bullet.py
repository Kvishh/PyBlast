import pygame, math, random
from configs import *
from game_map import tiles

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, target_x, target_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/images/enemy_projectile.png"), (BULLET_SIZE, BULLET_SIZE))
        self.rect = self.image.get_rect(center=(x, y))
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
    
    def update(self, dt, scroll):
        ########## TRAIL PARTICLE ##########
        for particle in self.particles:
            particle[0][0] -= 1
            particle[0][1] += particle[1]
        particle = [list(self.rect.midleft), random.uniform(-2, 2), pygame.Color(random.randrange(147, 206), 43, 207)]
        self.particles.append(particle)
        if len(self.particles) > 20:
            self.particles.pop(0)
        ########## TRAIL PARTICLE ##########
        self._draw_particles(scroll)

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
        for i, particle in enumerate(self.particles):
            pygame.draw.circle(display, particle[2], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), (i//3+2))

class SpecterEnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, target_x, target_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/images/enemy_projectile.png"), (BULLET_SIZE, BULLET_SIZE))
        self.rect = self.image.get_rect(center=(x, y))
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
    
    def update(self, dt, scroll):
        ########## TRAIL PARTICLE ##########
        for particle in self.particles:
            particle[0][0] -= 1
            particle[0][1] += particle[1]
        particle = [list(self.rect.midleft), random.uniform(-2, 2), (random.randrange(147, 206), 43, 207)]
        self.particles.append(particle)
        if len(self.particles) > 20:
            self.particles.pop(0)
        ########## TRAIL PARTICLE ##########
        self._draw_particles(scroll)

        if self.turn == 1:
            if self.opacity < 210:
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

    def _move(self, dt):
        self.pos.x += self._x_vel * dt
        self.pos.y += self._y_vel * dt
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

    def _draw_particles(self, scroll):
        for i, particle in enumerate(self.particles):
            radius = i//3+2
            circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

            pygame.draw.circle(circle, (particle[2][0], particle[2][1], particle[2][2], self.opacity), (radius, radius), radius)

            display.blit(circle, (particle[0][0]-scroll[0], particle[0][1]-scroll[1]))