import random

import pygame


class MyArrow:
    def __init__(self, img_path, screen_width=1600, screen_height=900,
                 size_x=150, size_y=150,x=1550,y=840,
                 horizontal_speed=10, frame_rate=50):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path).convert()
        self.img = pygame.transform.scale(self.img, (size_x, size_y))
        self.img.set_colorkey((255, 255, 255))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = self.img.get_rect()
        self.size_x = size_x
        self.size_y = size_y
        self.rect.x = screen_width
        self.rect.y = random.randint(self.screen_height-3*self.size_y, self.screen_height-self.size_y)
        self.horizontal_speed = horizontal_speed
        self.frame_rate = frame_rate
        self.mask = pygame.mask.from_surface(self.img)
        self.visited = False
        self.collapsed = False
        self.real_x = self.rect.x

    def horizontal_move(self):
        self.rect.x = self.rect.x - self.horizontal_speed*2
        self.real_x -= self.horizontal_speed

    def vertical_move(self):
        pass

    def get_mask(self):
        return self.mask

    def get_rect(self):
        return self.rect
