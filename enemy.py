import vector
from colors import *
import pygame
import compass

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, direction, health, radius, color):
        super().__init__()

        self.color = color.copy()
        self.pos = pos
        self.radius = radius
        self.speed = speed
        self.direction = direction
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.circle(self.image, color, (radius, radius), radius, )
        self.origin = pos[0] + radius, pos[1] + radius
        self.rect = self.image.get_rect()
        self.index = 0
        self.move_origin(pos)
        self.distance_travelled = 0
        self.start_health = health
        self.health = health

    def set_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.origin = pos[0] + self.radius, pos[1] + self.radius
        self.pos = pos

    def move_origin(self, pos):
        self.origin = pos
        self.pos = [self.origin[0] - self.radius, self.origin[1] - self.radius]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def apply_speed(self):
        movement = vector.times(self.speed, self.direction)
        new_pos = vector.plus(self.pos, movement)
        self.set_position(new_pos)
        self.distance_travelled += vector.mag(movement)

    def draw_image(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius, )

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
            self.die()

    def hit_bullet(self, game):
        if pygame.sprite.spritecollide(self, game.bullet_group, True):
            self.health += -1
            self.color[0] += 255 / self.start_health
            self.color[2] += -255 / self.start_health
            if self.color[2] < 0:
                self.die()
            else:
                self.draw_image()

    def die(self):
        self.kill()


class Boss(Enemy):
    def __init__(self, terrain):
        pos = terrain.start.origin
        tiles = terrain.surrounding_tiles(terrain.start, multiplier=2)
        for tile in tiles:
            if tile.color == road:
                direction = vector.unit(vector.distance(tile.pos, terrain.start.pos))
        super().__init__(pos, 1, direction, 10, 20, blue)