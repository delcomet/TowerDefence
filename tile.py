import vector
from colors import colors
import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, color, pos, size):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.size = size
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.pos = pos
        self.origin = [pos[0] + size / 2, pos[1] + size / 2]
        if color == colors['grass']:
            pygame.draw.line(self.image, colors['darkgreen'], [0, 0], [0, size], 1)
            pygame.draw.line(self.image, colors['darkgreen'], [0, 0], [size, 0], 1)
            pygame.draw.line(self.image, colors['darkgreen'], [0, size - 1], [size, size - 1], 1)
            pygame.draw.line(self.image, colors['darkgreen'], [size - 1, 0], [size - 1, size], 1)
