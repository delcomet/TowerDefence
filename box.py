import pygame


class Box(pygame.sprite.Sprite):
    def __init__(self, width, height, pos, color, alpha):
        super().__init__()
        self.width = width
        self.height = height
        self.pos = pos
        self.color = color.copy()
        self.alpha = alpha

        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)

    def add_text(self, pos, text, font_size, color, align='right'):
        font = pygame.font.SysFont("Comic Sans MS", font_size)
        text_image = font.render(text, True, color)
        if align == 'right':
            self.image.blit(text_image, pos)
        if align == 'center':
            self.image.blit(text_image, [pos[0] - text_image.get_width()/2, pos[1] - text_image.get_height()/2])
        if align == 'left':
            self.image.blit(text_image, [pos[0] - text_image.get_width(), pos[1]])
