import vector
from colors import *
from pygame.constants import *
import pygame

from bullet import Bullet

class BasicTower(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, image_file):
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(grass)
        self.image.set_colorkey(grass)
        self.rect = self.image.get_rect()
        self.set_position(pos)

        self.active_state = 1

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
        self.range_color = red.copy()
        transparent = (123, 123, 123)
        self.range_image.fill(transparent)
        self.range_image.set_colorkey(transparent)
        self.range_image.set_alpha(100)

    def set_position(self, pos):
        self.origin = [pos[0] + self.width / 2, pos[1] + self.height / 2]
        self.rect.x, self.rect.y = pos







class Tower(pygame.sprite.Sprite):
    def __init__(self, game, width, height, image_file):
        super().__init__()
        self.game = game
        self.width = width * game.map.tile_size
        self.height = height * game.map.tile_size
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(grass)
        self.image.set_colorkey(grass)
        self.rect = self.image.get_rect()
        self.set_position(pygame.mouse.get_pos())

        self.barrel_axis = None
        self.range = 0
        self.bullet_speed = 0
        self.cooldown = 0
        self.timer = 0
        self.active_state = 1

        self.original_cannon_image = pygame.image.load(image_file).convert_alpha()
        self.original_cannon_image = pygame.transform.scale(self.original_cannon_image, [self.width, self.height])
        self.original_cannon_image_rect = self.original_cannon_image.get_rect()
        self.rotated_cannon = self.original_cannon_image

        self.range_image = pygame.Surface([self.range * 2, self.range * 2])
        self.range_image_rect = self.range_image.get_rect()
        self.range_color = red.copy()
        self.range_image.fill(grass)
        self.range_image.set_colorkey(grass)
        self.range_image.set_alpha(100)

    def setup_turret(self, fire_range, bullet_speed, cooldown, barrel_axis):
        self.range = fire_range
        self.bullet_speed = bullet_speed
        self.cooldown = cooldown
        self.timer = cooldown
        self.barrel_axis = barrel_axis

        self.range_image = pygame.Surface([self.range * 2, self.range * 2])
        self.range_image_rect = self.range_image.get_rect()
        self.range_color = red.copy()
        transparent = (123, 123, 123)
        self.range_image.fill(transparent)
        self.range_image.set_colorkey(transparent)
        self.range_image.set_alpha(100)

    def set_position(self, pos):
        self.pos = pos
        self.origin = [pos[0] + self.width / 2, pos[1] + self.height / 2]
        self.rect.x, self.rect.y = pos

    def active(self, state=1):
        self.active_state = state

    def handle_event(self, event, mouse):
        if event is not None:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(mouse):
                        self.active_state = not self.active_state
                    else:
                        self.active_state = 0
        if len(self.game.map.moving_tower_group.sprites()) > 0:
            for tile in self.game.map.tiles:
                if tile.rect.collidepoint(mouse[0] - self.width / 4, mouse[1] - self.height / 4):
                    self.game.map.moving_tower_group.sprites()[0].set_position([tile.rect.x, tile.rect.y])
                    if pygame.sprite.spritecollide(self, self.game.map.roads, False):
                        self.range_color = red
                    elif pygame.sprite.spritecollide(self, self.game.map.static_tower_group, False):
                        self.range_color = red
                    elif pygame.sprite.spritecollide(self, self.game.map.bases, False):
                        self.range_color = red
                    else:
                        self.range_color = white

    def update(self):
        if self.game.map.static_tower_group.has(self):
            self.enemy_detection()
        if self.game.map.moving_tower_group.has(self):
            self.active_state = 1

        for sprite in self.game.map.static_tower_group:
            sprite.range_color = white

        remainder_x = self.rect.x + self.rect.width - self.game.map.pixel_size[0]
        remainder_y = self.rect.y + self.rect.height - self.game.map.pixel_size[1]
        if remainder_x > 0:
            self.set_position([self.pos[0] - remainder_x, self.pos[1]])
        if remainder_y > 0:
            self.set_position([self.pos[0], self.pos[1] - remainder_y])

    def draw_images(self, window):
        self.image.fill(grass)
        self.image.blit(self.rotated_cannon, [0, 0])
        if self.active_state == 1:
            pygame.draw.circle(self.range_image, self.range_color,
                               [self.range_image_rect.centerx, self.range_image_rect.centery], self.range)
            window.blit(self.range_image, [self.origin[0] - self.range, self.origin[1] - self.range])

    def enemy_detection(self):
        self.timer += 1 / self.game.fps
        on_range = []
        distance_travelled_list = []

        for enemy in self.game.map.enemy_group:
            distance_vector = vector.distance(enemy.origin, self.origin)
            mag = vector.mag(distance_vector)
            if mag < self.range + enemy.radius:
                on_range.append(enemy)
        if len(on_range) == 0:
            return
        for on_range_enemy in on_range:
            distance_travelled_list.append(on_range_enemy.distance_travelled)
        for on_range_enemy in on_range:        
            if on_range_enemy.distance_travelled == max(distance_travelled_list):
                self.aim(on_range_enemy)
                self.rotate_cannon(on_range_enemy)

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
        return rot_image

    def aim(self, enemy):
        distance_vector = vector.distance(enemy.origin, self.origin)
        mag = vector.mag(distance_vector)
        unit_vector = vector.times(1 / mag, distance_vector)
        speed_vector = vector.times(self.bullet_speed, unit_vector)
        if self.cooldown < self.timer:
            self.fire(speed_vector)
            self.timer = 0

    def fire(self, speed_vector):
        # TODO: return bullet
        bullet = Bullet(self.origin, speed_vector)
        self.game.map.bullet_group.add(bullet)


class CannonTower(Tower):
    def __init__(self, game):
        super().__init__(game, 2, 2, 'data/images/cannon.png')
        self.setup_turret(100, 10, 0.1, [0, -1])


class ArtilleryTower(Tower):
    def __init__(self, game):
        super().__init__(game, 3, 3, 'data/images/artillery.png')
        self.setup_turret(200, 30, 1, [0, -1])