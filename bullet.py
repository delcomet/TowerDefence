import vector
from colors import colors
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, speed):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill(colors['black'])
        self.rect = self.image.get_rect()
        self.speed = speed
        self.pos = start_pos
        self.set_position(self.pos)

    def set_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pos

    def apply_speed(self):
        self.pos = vector.plus(self.pos, self.speed)
        self.set_position(self.pos)

    def check_borders(self, terrain):
        if self.pos[0] < self.rect.width or self.pos[1] < self.rect.height or self.pos[0] > terrain.pixel_size[0] or \
                        self.pos[1] > terrain.pixel_size[1]:
            self.kill()

    def update(self, terrain):
        self.apply_speed()
        self.check_borders(terrain)