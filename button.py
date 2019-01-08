import pygame
from colors import colors
from pygame.constants import *
from textbox import TextBox

def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

class Button(pygame.sprite.Sprite):

    description = ''
    hovering = False
    locked = False
    blurred_icon = False

    def __init__(self, color, width, height):
        super().__init__()
        self.color = list(color)
        self.width = width
        self.height = height

        self.normal_image = pygame.image.load("data/images/normal_button.png").convert_alpha()
        self.normal_image = pygame.transform.smoothscale(self.normal_image, [self.width, self.height])
        self.pressed_image = pygame.image.load("data/images/pressed_button.png")
        self.pressed_image = pygame.transform.smoothscale(self.pressed_image, [self.width, self.height])
        self.hover_image = pygame.image.load("data/images/hover_button.png")
        self.hover_image = pygame.transform.smoothscale(self.hover_image, [self.width, self.height])

        self.image = self.normal_image.copy()
        self.rect = self.image.get_rect()
        self.set_position((0, 0))

        self.icon_pos = (0, 0)
        self.icon = pygame.Surface((0, 0))

    def set_description(self, description, textbox):
        self.description = description
        self.description_box = textbox

    def set_position(self, pos):
        self.rect.x, self.rect.y = pos

    def set_icon_image(self, image, size):
        width, height = size
        self.icon = pygame.image.load(image)
        self.icon = pygame.transform.smoothscale(self.icon, (width, height))
        self.blurred_icon = blurSurf(self.icon, 10)
        self.icon_pos = [self.rect.width/2 - width/2, self.rect.height/2 - height/2]
        self.image.blit(self.icon, self.icon_pos)

    def set_icon_text(self, text, font_size=20):
        textbox = TextBox(self.width, self.height)
        textbox.add_text(text, align="center", font_size=font_size, color=colors['black'])
        
        self.icon = textbox.image
        self.blurred_icon = self.icon.copy()
        image = pygame.Surface([self.width, self.height])
        image.fill(colors['gray'])
        image.set_alpha(240)
        self.blurred_icon.blit(image, (0,0))
        self.icon_pos = [self.rect.width/2 - self.width/2, self.rect.height/2 - self.height/2]
        self.image.blit(self.icon, self.icon_pos)

    def update(self, event=None):
        if event is not None and not self.locked:
            if event.type == MOUSEMOTION:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.on_hover()
                    self.draw(self.hover_image)
                elif self.hovering:
                    self.unhover()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.draw(self.pressed_image)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.function()
                    self.draw(self.normal_image)


    def on_hover(self):
        self.hovering = True
        if self.description:
            self.description_box.add_text(self.description, align="center")

    def unhover(self):
        self.hovering = False
        self.draw(self.normal_image)
        if self.description:
            self.description_box.default_text()

    def lock(self):
        self.locked = True
        self.draw(self.pressed_image)
        if self.blurred_icon:
            self.image.blit(self.blurred_icon, self.icon_pos)

    def unlock(self):
        self.locked = False
        self.draw(self.normal_image)
        if self.blurred_icon:
            self.image.blit(self.icon, self.icon_pos)

    def function(self):
        pass

    def draw(self, image):
        self.image = image.copy()
        self.image.blit(self.icon, self.icon_pos)

    
class TowerButton(Button):
    def __init__(self, TowerClass, terrain, info_box):
        super().__init__(colors['white'], 60, 60)
        self.TowerClass = TowerClass
        self.terrain = terrain
        self.info_box = info_box
        self.set_icon_image(TowerClass.icon_file, TowerClass.icon_size)
        self.set_description(TowerClass.description, info_box)
    
    def function(self):
        self.terrain.moving_tower_group.add(self.TowerClass(self.terrain))


