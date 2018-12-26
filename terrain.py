
import vector
from colors import *
from pygame.constants import *
import pygame
import compass
import math
from tile import Tile

class terrain:
    def __init__(self, terrain_name):
        self.tile_size = 20
        self.start = None
        self.end = None
        
        self.tiles = pygame.sprite.OrderedUpdates()   
        self.bases = pygame.sprite.Group()
        self.roads = pygame.sprite.Group()     

        self.setup_terrain(terrain_name)

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

        tiles_loaded = str(len(self.tiles))
        window_in_tiles = str(self.width * self.height)
        if tiles_loaded != window_in_tiles:
            raise ValueError("Number of tiles loaded ({}) doesn't match the window size ({})".format(tiles_loaded, window_in_tiles))


        self.static_tower_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.moving_tower_group = pygame.sprite.GroupSingle()

    def available_space(self, sprite):
        if pygame.sprite.spritecollide(sprite, self.roads, False):
            return False
        elif pygame.sprite.spritecollide(sprite, self.static_tower_group, False):
            return False
        elif pygame.sprite.spritecollide(sprite, self.bases, False):
            return False
        else:
            return True

    def get_tile(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.pixel_size[0] or pos[1] > self.pixel_size[1]:
            return Tile([0, 0, 0], pos, 0)

        row = math.floor(pos[1] / self.tile_size)
        column = math.floor(pos[0] / self.tile_size)

        sprites = self.tiles.sprites()
        index = row * self.width + column

        if len(sprites) > index:
            return sprites[index]
        else:
            return Tile([0, 0, 0], pos, 0)

    def surrounding_tiles(self, tile, multiplier=1):
        surrounding = []
        for direction in compass.DIRECTIONS:
            distance = vector.times(self.tile_size * multiplier, direction)
            pos = vector.plus(tile.origin, distance)
            found_tile =  self.get_tile(pos)
            if found_tile.size != 0:
                surrounding.append(found_tile)
        return surrounding




    def setup_terrain(self, terrain_name):
        x = 0
        y = 0
        index = 0

        with open(terrain_name) as f:
            terrain_lines = f.readlines()


        self.width = (len(terrain_lines[0]) - 1)
        self.height = (len(terrain_lines))

        for line in terrain_lines:
            width = 0
            for digit in line:

                if digit == '0':
                    created_tile = Tile(grass, [x, y], self.tile_size)

                elif digit == '1':
                    created_tile = Tile(road, [x, y], self.tile_size)
                    self.roads.add(created_tile)

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





    def draw(self, window):
        self.tiles.draw(window)
        self.bases.draw(window)
        self.enemy_group.draw(window)
        self.bullet_group.draw(window)
        self.static_tower_group.draw(window)
        for tower in self.static_tower_group:
            tower.draw_images(window)

        self.moving_tower_group.draw(window)
        for tower in self.moving_tower_group:
            tower.draw_images(window)        