import pygame
from colors import colors

class TextBox(pygame.sprite.Sprite):
    def __init__(self, width, height, bgcolor=None, alpha=250):
        super().__init__()
        self.width = width
        self.height = height
        
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()

        if bgcolor:
            self.bgcolor = list(bgcolor)
        else:
            self.bgcolor = (250, 250, 250)
            self.image.set_colorkey(self.bgcolor)

        self.image.fill(self.bgcolor)
        self.image.set_alpha(alpha)

    def set_position(self, pos):
        self.rect.x, self.rect.y = pos

    def set_center(self, pos):
        self.rect.centerx, self.rect.centery = pos

    def add_text(self, text, font_size=20, color=colors['black'], align='right'):
        self.image.fill(self.bgcolor)
        font = pygame.font.SysFont("Comic Sans MS", font_size)
        size = font.size(text)
        lines = self.split_lines(text, font)
        self.blit_lines(lines, font, color, align)

    def add_default_text(self, *args, **kwargs):
        self.default_args = args
        self.default_kwargs = kwargs
        self.add_text(*args, **kwargs)

    def default_text(self):
        self.add_text(*self.default_args, **self.default_kwargs)

    def blit_lines(self, lines, font, color, align):
        

        height = font.size(lines[0])[1]
        x = 0
        y = 0
        for line in lines:
            text_image = font.render(line, True, color)
            if align == 'right':
                self.image.blit(text_image, (x, y))
            if align == 'center':
                self.image.blit(text_image, [(self.width - text_image.get_width()) / 2, y])
            if align == 'left':
                self.image.blit(text_image, [self.width - text_image.get_width(), y])
            y += height

    def split_lines(self, text, font):
        original_lines = text.splitlines()
        lines = []
        for original_line in original_lines:
            if font.size(original_line)[0] > self.width:
                words = original_line.split(" ")
                line = ""
                for word in words:
                    if font.size(line + word + " ")[0] > self.width:
                        lines.append(str(line))
                        line = ""
                    line += (word + " ")
                if line:
                    lines.append(line)
            else:
                lines.append(original_line)
        return lines

    
