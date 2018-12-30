import vector
from colors import *
import pygame
import compass
import math

class Enemy(pygame.sprite.Sprite):

    distance_travelled = 0
    bar_distance = 8

    def __init__(self, pos, speed, direction, health, radius, color):
        super().__init__()
        self.color = color.copy()
        self.radius = radius
        self.speed = speed
        self.direction = direction
        self.start_health = health
        self.health = health

        self.image = pygame.Surface([radius * 2, radius * 2 + self.bar_distance])
        self.image.fill(white)
        self.image.set_colorkey(white)
        self.draw_image()
        self.rect = self.image.get_rect()

        self.set_origin(pos)

    def set_position(self, pos):
        self.rect.x = pos[0] 
        self.rect.y = pos[1] - self.bar_distance
        self.origin = (pos[0] + self.radius, pos[1] + self.radius)
        self.pos = tuple(pos)

    def set_origin(self, pos):
        self.set_position([pos[0] - self.radius, pos[1] - self.radius])
        

    def apply_speed(self):
        movement = vector.times(self.speed, self.direction)
        new_pos = vector.plus(self.pos, movement)
        self.set_position(new_pos)
        self.distance_travelled += vector.mag(movement)

    def draw_image(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius + self.bar_distance), self.radius, )
        bar_lenght = self.radius*2
        pygame.draw.line(self.image, red, (0, 0), (bar_lenght, 0), 8)
        end = (bar_lenght * (self.health / self.start_health), 0)
        pygame.draw.line(self.image, green, (0, 0), end, 8)


    def move_in_terrain(self, terrain):
        if not self.can_go(terrain, self.direction):
            new_direction = vector.perpendicular(self.direction)
            if not self.can_go(terrain, new_direction):
                new_direction = vector.reverse(new_direction)
            self.direction = new_direction

    def can_go(self, terrain, direction):
        distance_vector = vector.times(1.5 * terrain.tile_size + 1, direction)
        tile_pos = vector.plus(distance_vector, self.origin)
        tile = terrain.get_tile(tile_pos)
        if tile.color == grass:
            return False
        else:
            return True


    def hit_base(self, terrain):
        if pygame.sprite.collide_rect(self, terrain.end):
            self.kill()

    def update(self, terrain):
        self.apply_speed()
        self.move_in_terrain(terrain)
        self.hit_base(terrain)
        self.check_health()
        self.hit_bullet(terrain)

    def check_health(self):
        if self.health <= 0:
            self.kill()

    def hit_bullet(self, game):
        if pygame.sprite.spritecollide(self, game.bullet_group, True):
            self.health += -1
            self.color[0] += 255 / self.start_health
            self.color[2] += -255 / self.start_health
            if self.color[2] < 0:
                self.kill()
            else:
                self.draw_image()


class Boss(Enemy):
    def __init__(self, terrain):
        pos = terrain.start.origin
        tiles = terrain.surrounding_tiles(terrain.start, multiplier=2)
        for tile in tiles:
            if tile.color == road:
                direction = vector.unit(vector.distance(tile.pos, terrain.start.pos))
        super().__init__(pos, 1, direction, 10, 20, blue)