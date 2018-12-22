import vector
from colors import *
import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, color, pos, size):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.size = size
        self.color = color.copy()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.origin = [pos[0] + size / 2, pos[1] + size / 2]
        self.index = 0
        if self.color == grass:
            pygame.draw.line(self.image, darkgreen, [0, 0], [0, size], 1)
            pygame.draw.line(self.image, darkgreen, [0, 0], [size, 0], 1)
            pygame.draw.line(self.image, darkgreen, [0, size - 1], [size, size - 1], 1)
            pygame.draw.line(self.image, darkgreen, [size - 1, 0], [size - 1, size], 1)
