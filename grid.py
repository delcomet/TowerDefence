

import pygame
from pygame.sprite import Sprite
import math

class GridGroup(pygame.sprite.OrderedUpdates):

    def __init__(self, pos, cols=3, rows=3,  margin=0.0):
        super().__init__()

        self.x, self.y = pos
        self.cols = cols
        self.rows = rows
        self.margin = margin

        self.col_width = 0
        self.row_height = 0

    def append(self, sprite):
        for row in range(self.rows):
            for column in range(self.cols):
                if not self.get_sprite(row, column):
                    self.insert(sprite, row, column)
                    return
        raise Exception("Grid is full")

    def insert(self, sprite, row, column):
        index = row * self.rows + column

        if self.col_width < sprite.rect.width:
            height = self.row_height if self.row_height else sprite.rect.height
            self.resize(sprite.rect.width, height)
        if self.row_height < sprite.rect.height:
            width = self.col_width if self.col_width else sprite.rect.width
            self.resize(width, sprite.rect.height)

        self.position_sprite(sprite, row, column)

        self.add_internal(sprite, index)
        sprite.add_internal(self)

            

    def get_sprite(self, row, column):
        sprites = self.sprites()
        index = row * self.rows + column
        try:
            return sprites[index]
        except IndexError:
            return None

    def add_internal(self, sprite, index):
        self.spritedict[sprite] = 0
        self._spritelist.insert(index, sprite)

    def resize(self, width, height):
        self.col_width = width
        self.row_height = height
        for row in range(self.rows):
            for column in range(self.cols):
                sprite = self.get_sprite(row, column)
                if sprite:
                    self.position_sprite(sprite, row, column)
                    

    def position_sprite(self, sprite, row, column):
        x = column * (self.col_width + self.margin) + self.x
        y = row * (self.row_height + self.margin) + self.y

        sprite.rect.x = x
        sprite.rect.y = y

    def add(self, *sprites):
        """add sprite(s) to group

        Group.add(sprite, list, group, ...): return None

        Adds a sprite or sequence of sprites to a group.

        """
        for sprite in sprites:
            # It's possible that some sprite is also an iterator.
            # If this is the case, we should add the sprite itself,
            # and not the iterator object.
            if isinstance(sprite, Sprite):
                if not self.has_internal(sprite):
                    self.append(sprite)
            else:
                try:
                    # See if sprite is an iterator, like a list or sprite
                    # group.
                    self.add(*sprite)
                except (TypeError, AttributeError):
                    # Not iterable. This is probably a sprite that is not an
                    # instance of the Sprite class or is not an instance of a
                    # subclass of the Sprite class. Alternately, it could be an
                    # old-style sprite group.
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if not self.has_internal(spr):
                                self.append(spr)
                    elif not self.has_internal(sprite):
                        self.append(sprite)




        


