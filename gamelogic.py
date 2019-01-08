import pygame
import vector
import button
from textbox import TextBox 
from pygame.constants import *
from colors import colors
from grid import GridGroup

from tile import Tile
from towers import CannonTower, ArtilleryTower
from enemy import Boss
from terrain import Terrain

def get_active(group):
    for sprite in group:
        if sprite.active:
            return sprite
    return pygame.sprite.Sprite()


class Game:
    clock = pygame.time.Clock()
    fps = 120

    def __init__(self, terrain_name):
        pygame.init()

        self.terrain = Terrain(terrain_name)
        self.window_size = [self.terrain.pixel_size[0] + 250, self.terrain.pixel_size[1] + 150]
        self.window = pygame.display.set_mode(self.window_size)

        self.init_content()


    def init_content(self):
        info_box = TextBox(200, 400, bgcolor=colors['white'], alpha=150)
        info_box.set_position([self.terrain.pixel_size[0] + 25, 250])
        info_box.add_default_text("Tower Defence\n\nPlace turrets on the map to protect your base from enemies. You gain money by winning rounds and killing enemies.", align="center")
        self.box_group = pygame.sprite.Group(info_box)

        cannon_button = button.TowerButton(CannonTower, self.terrain, info_box)
        artillery_button = button.TowerButton(ArtilleryTower, self.terrain, info_box)


        self.tower_buttons = GridGroup(pos=[self.terrain.pixel_size[0] + 25, 15], cols=3, rows=3, margin=10)
        self.tower_buttons.add(cannon_button, artillery_button)


        for _ in range(7):
            empty = button.Button(colors['white'], 60, 60)
            self.tower_buttons.add(empty)
            empty.lock()

        start_button = button.Button(colors['green'], 200, 90)
        start_button.set_position((self.terrain.pixel_size[0] + 25, 670))
        start_button.set_icon_text("Start", font_size=50)
        start_button.set_description("Start round 1", info_box)

        self.description = info_box
        self.buttons = pygame.sprite.Group(start_button)



    def mainloop(self):
        while True:

            mouse = pygame.mouse.get_pos()
            # if self.terrain.get_tile(mouse).size:
            #     self.description.default_text()

            for event in pygame.event.get():
                self.tower_buttons.update(event)
                self.buttons.update(event)
                self.terrain.handle_event(event, mouse)
                self.handle_event(event)

            # Logic testing:
            self.terrain.update()

            # Draw everything:
            self.draw_everything()

            # Delay framerate and update display:
            self.clock.tick(self.fps)
            pygame.display.flip()


    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.terrain.enemy_group.add(Boss(self.terrain))
            elif event.key == K_r:
                self.terrain.static_tower_group.empty()
                self.terrain.enemy_group.empty()
            elif event.key == K_DELETE:
                get_active(self.terrain.static_tower_group).kill()

    def draw_everything(self):
        self.window.fill(colors['background'])
        self.terrain.draw(self.window)
        self.tower_buttons.draw(self.window)
        self.buttons.draw(self.window)
        self.box_group.draw(self.window)

        
        