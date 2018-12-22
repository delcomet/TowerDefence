
import vector
from colors import *
from pygame.constants import *
import pygame
from tile import Tile

class Map:
    def __init__(self, map_name):
        self.tile_size = 20
        self.start = None
        self.end = None
        
        self.tiles = pygame.sprite.OrderedUpdates()   
        self.checkpoints = pygame.sprite.Group()
        self.bases = pygame.sprite.Group()
        self.roads = pygame.sprite.Group()     

        self.setup_map(map_name)

        self.pixel_size = [self.tile_size * self.width, self.tile_size * self.height]

        self.end.image = pygame.Surface([60, 100])
        self.end.pos = self.end.origin
        self.end.rect = self.end.image.get_rect()
        self.end.rect.x = self.end.pos[0] - self.end.image.get_width() / 2
        self.end.rect.y = self.end.pos[1] - self.end.image.get_height() / 2
        remainder = self.end.rect.x + self.end.image.get_width() - self.tile_size * self.width
        if remainder > 0:
            self.end.rect.x += -remainder

        self.end.image.fill(black)

        for block in self.checkpoints:
            if block.rect.x == self.start.rect.x or block.rect.y == self.start.rect.y:
                a = [block.pos[0] - self.start.pos[0], block.pos[1] - self.start.pos[1]]
                mag = vector.mag(a)
                self.starting_vector = vector.times(1 / mag, a)

        tiles_loaded = str(len(self.tiles))
        window_in_tiles = str(self.width * self.height)
        if tiles_loaded != window_in_tiles:
            raise ValueError("Number of tiles loaded ({}) doesn't match the window size ({})".format(tiles_loaded, window_in_tiles))


        self.static_tower_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.moving_tower_group = pygame.sprite.GroupSingle()



    def setup_map(self, map_name):
        x = 0
        y = 0
        index = 0

        with open(map_name) as f:
            map_lines = f.readlines()


        self.width = (len(map_lines[0]) - 1)
        self.height = (len(map_lines))

        for line in map_lines:
            width = 0
            for digit in line:

                if digit == '0':
                    created_tile = Tile(grass, [x, y], self.tile_size)

                elif digit == '1':
                    created_tile = Tile(road, [x, y], self.tile_size)
                    self.roads.add(created_tile)

                elif digit == '2':
                    created_tile = Tile(road, [x, y], self.tile_size)
                    self.checkpoints.add(created_tile)

                elif digit == '8':
                    created_tile = Tile(green, [x, y], self.tile_size)
                    self.start = created_tile
                    self.bases.add(created_tile)

                elif digit == '9':
                    created_tile = Tile(red, [x, y], self.tile_size)
                    self.end = created_tile
                    self.bases.add(self.end)
                else:
                    continue
                    
                created_tile.index = index
                self.tiles.add(created_tile)
                width += 1
                x += self.tile_size
                index += 1
                

            x = 0
            y += self.tile_size

    def update(self):
        # Update functions:
        self.enemy_group.update(self)
        self.bullet_group.update(self)
        self.static_tower_group.update()
        self.moving_tower_group.update()

    def handle_event(self, event, mouse):
        for tower in self.static_tower_group:
            tower.handle_event(event, mouse)
        for tower in self.moving_tower_group:
            tower.handle_event(event, mouse)
        if event is not None:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.try_drop_tower(mouse)


    def try_drop_tower(self, mouse):
        if len(self.moving_tower_group) > 0:
            if self.moving_tower_group.sprites()[0].rect.collidepoint(mouse):
                if self.moving_tower_group.sprites()[0].range_color == white:
                    self.static_tower_group.add(self.moving_tower_group.sprites()[0])
                    self.moving_tower_group.empty()
            else:
                self.moving_tower_group.sprites()[0].kill()

    def draw(self, window):
        self.tiles.draw(window)
        self.bases.draw(window)
        self.enemy_group.draw(window)
        self.bullet_group.draw(window)
        self.static_tower_group.draw(window)
        for tower in self.static_tower_group:
            tower.draw_images(window)

        self.moving_tower_group.draw(window)
        for tower in self.moving_tower_group.sprites():
            tower.draw_images(window)        