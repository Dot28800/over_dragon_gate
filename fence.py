import random

import pygame


class Fence:
    def __init__(self, img_path,
                 screen_width=1600, screen_height=900,
                 x=1550,y=840,
                 size_x=20, size_y=60,
                 speed=10):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path).convert()
        self.img.set_colorkey((0, 0, 0))
        self.img = pygame.transform.scale(self.img, (size_x, size_y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = self.img.get_rect()
        self.size_x=size_x
        self.size_y=size_y
        self.rect.x =x
        self.rect.y =y
        self.real_x=x
        self.speed=speed
        self.mask = pygame.mask.from_surface(self.img)
        self.visited=False
        self.collapsed=False
    def horizontal_move(self):
        self.rect.x -= self.speed

    def vertical_move(self):
        pass
    def get_mask(self):
        return self.mask

    def get_rect(self):
        return self.rect

