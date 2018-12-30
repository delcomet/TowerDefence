import pygame
from colors import *
from pygame.constants import *

class Button(pygame.sprite.Sprite):

    def __init__(self, color, width, height, pos, alpha=255):
        super().__init__()
        self.color = color.copy()
        self.width = width
        self.height = height
        self.pos = pos
        self.alpha = alpha

        self.normal_image = pygame.image.load("data/images/normal_button.png").convert_alpha()
        self.normal_image = pygame.transform.smoothscale(self.normal_image, [self.width, self.height])
        self.pressed_image = pygame.image.load("data/images/pressed_button.png")
        self.pressed_image = pygame.transform.smoothscale(self.pressed_image, [self.width, self.height])
        self.hover_image = pygame.image.load("data/images/hover_button.png")
        self.hover_image = pygame.transform.smoothscale(self.hover_image, [self.width, self.height])

        self.image = self.normal_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

        self.icon = pygame.Surface((0, 0))
        self.icon_pos = [0, 0]

        self.hovering_state = 0

    def set_icon_image(self, image, width, height):
        self.icon = pygame.image.load(image)
        self.icon = pygame.transform.smoothscale(self.icon, (width, height))
        self.icon_pos = [self.rect.width/2 - width/2, self.rect.height/2 - height/2]
        self.image.blit(self.icon, self.icon_pos)

    def set_icon_text(self):
        pass

    def update(self, event=None):
        if event is not None:
            if event.type == MOUSEMOTION:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.hover(1)
                else:
                    self.hover(0)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.press(1)
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.function()
                        self.press(0)
                    else:
                        self.press(0)

    def function(self):
        pass

    def press(self, value=1):
        if value is 1:
            self.image = self.pressed_image.copy()
            self.image.blit(self.icon, self.icon_pos)

        if value is 0:
            self.image = self.normal_image.copy()
            self.image.blit(self.icon, self.icon_pos)

    def hover(self, value=1):
        if value is 1:
            self.hovering_state = 1
            self.image = self.hover_image.copy()
            self.image.blit(self.icon, self.icon_pos)

        if value is 0:
            self.hovering_state = 0
            self.image = self.normal_image.copy()
            self.image.blit(self.icon, self.icon_pos)


