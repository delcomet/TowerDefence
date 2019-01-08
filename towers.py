import vector
import strategy
from colors import colors
from pygame.constants import *
import pygame
from pygame import Rect
import time
from helpers import *

from bullet import Bullet

class Tower(pygame.sprite.Sprite):
    last_shot = 0
    static = False 
    active = True

    def __init__(self, terrain, width, height, image_file):
        super().__init__()
        self.terrain = terrain
        self.width = width * terrain.tile_size
        self.height = height * terrain.tile_size
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colors['grass'])
        self.image.set_colorkey(colors['grass'])
        self.rect = self.image.get_rect()
        self.set_position(pygame.mouse.get_pos())

        self.original_cannon_image = pygame.image.load(image_file).convert_alpha()
        self.original_cannon_image = pygame.transform.scale(self.original_cannon_image, [self.width, self.height])
        self.original_cannon_image_rect = self.original_cannon_image.get_rect()
        self.rotated_cannon = self.original_cannon_image


    def setup_turret(self, fire_range, bullet_speed, cooldown, barrel_axis):
        self.range = fire_range
        self.bullet_speed = bullet_speed
        self.cooldown = cooldown
        self.timer = cooldown
        self.barrel_axis = barrel_axis

        self.range_image = pygame.Surface([self.range * 2, self.range * 2])
        self.range_image_rect = self.range_image.get_rect()
        self.range_color = colors['red']
        transparent = (123, 123, 123)
        self.range_image.fill(transparent)
        self.range_image.set_colorkey(transparent)
        self.range_image.set_alpha(100)

    def set_position(self, pos):
        self.pos = pos
        self.origin = [pos[0] + self.width / 2, pos[1] + self.height / 2]
        self.rect.x, self.rect.y = pos

        remainder_x = self.rect.x + self.rect.width - self.terrain.pixel_size[0]
        remainder_y = self.rect.y + self.rect.height - self.terrain.pixel_size[1]
        if remainder_x > 0:
            self.set_position([self.pos[0] - remainder_x, self.pos[1]])
        if remainder_y > 0:
            self.set_position([self.pos[0], self.pos[1] - remainder_y])


    def handle_event(self, event, mouse):
        if event is None:
            return
        if self.static:
            if left_click(event):
                self.on_click(mouse)
                    
        if not self.static:
            if event.type == MOUSEMOTION:
                self.follow_mouse(mouse)
            elif left_click(event):
                self.drop_on_map(mouse)
            elif right_click(event):
                self.kill()

    def follow_mouse(self, mouse):
        tile = self.terrain.get_tile((mouse[0] - self.width / 4, mouse[1] - self.height / 4))
        if tile.size:
            self.set_position(tile.pos)

        if self.terrain.available_space(self):
            self.range_color = colors['white']
        else:
            self.range_color = colors['red']
        

    def drop_on_map(self, mouse):
        if self.rect.collidepoint(mouse) and self.range_color == colors['white']:
            self.static = True
            self.terrain.static_tower_group.add(self)
            self.terrain.moving_tower_group.empty()

    def on_click(self, mouse):
        if self.rect.collidepoint(mouse):
            self.active = not self.active
        else:
            self.active = False


    def update(self):
        if self.static:
            self.enemy_detection()


    def draw_images(self, window):
        self.image.fill(colors['grass'])
        self.image.blit(self.rotated_cannon, [0, 0])
        if self.active:
            pygame.draw.circle(self.range_image, self.range_color,
                               [self.range_image_rect.centerx, self.range_image_rect.centery], self.range)
            window.blit(self.range_image, [self.origin[0] - self.range, self.origin[1] - self.range])

    def enemy_detection(self):
        target = self.find_target(strategy.longest_distance)
        if target:
            self.rotate_cannon(target)
            direction = self.aim(target)
            if self.ready():
                self.terrain.bullet_group.add(self.fire(direction))

    def find_target(self, strategy):
        return strategy(self.enemies_on_range())

    def enemies_on_range(self):
        on_range = []
        for enemy in self.terrain.enemy_group:
            distance_vector = vector.distance(enemy.origin, self.origin)
            mag = vector.mag(distance_vector)
            if mag < self.range + enemy.radius:
                on_range.append(enemy)
        return on_range

    def rotate_cannon(self, enemy):
        distance_vector = vector.distance(enemy.origin, self.origin)
        angle = vector.angle(self.barrel_axis, distance_vector)
        if distance_vector[0] > 0:
            angle *= -1
        rot_image = pygame.transform.rotate(self.original_cannon_image, angle)
        rot_rect = self.original_cannon_image_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.rotated_cannon = rot_image

    def aim(self, enemy):
        distance_vector = vector.distance(enemy.origin, self.origin)
        mag = vector.mag(distance_vector)
        unit_vector = vector.times(1 / mag, distance_vector)
        return vector.times(self.bullet_speed, unit_vector)
        

    def fire(self, speed_vector):
        self.last_shot = pygame.time.get_ticks()
        return Bullet(self.origin, speed_vector)

    def ready(self):
        time_passed = pygame.time.get_ticks() - self.last_shot
        boolean = time_passed > self.cooldown * 1000
        return boolean



class CannonTower(Tower):
    
    description = "Cannon Tower"
    icon_file = 'data/images/cannon.png'
    icon_size = (40, 40)

    def __init__(self, terrain):

        super().__init__(terrain, 2, 2, self.icon_file)
        self.setup_turret(fire_range=100, bullet_speed=10, cooldown=0.5, barrel_axis=[0, -1])


class ArtilleryTower(Tower):
    
    description = "Artillery Tower"
    icon_file = 'data/images/artillery.png'
    icon_size = (55, 55)

    def __init__(self, terrain):

        super().__init__(terrain, 3, 3, self.icon_file)
        self.setup_turret(fire_range=200, bullet_speed=30, cooldown=1, barrel_axis=[0, -1])


