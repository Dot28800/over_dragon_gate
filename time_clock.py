import random

import pygame
from math import sin,cos,pi

class TimeClock:
    def __init__(self, img_path,screen_width=1600, screen_height=900,
                 size_x=150, size_y=150,
                 horizontal_speed=10,frame_rate=50):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path).convert()
        self.img = pygame.transform.scale(self.img, (size_x, size_y))
        self.img.set_colorkey((255, 255, 255))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = self.img.get_rect()
        self.rect.x= screen_width
        self.rect.y= screen_height - 2 * size_y
        self.size_x = size_x
        self.size_y = size_y
        self.horizontal_speed = horizontal_speed
        self.frame_rate = frame_rate
        self.mask = pygame.mask.from_surface(self.img)
        self.visited = False
        self.collapsed = False
        self.radius = 0.25*self.size_y
        self.angle_velocity= 2*pi
        self.phase=2*pi* random.random()
        self.real_x= self.rect.x

    def horizontal_move(self):
        self.rect.x = self.rect.x - self.horizontal_speed - self.angle_velocity*self.radius*sin(self.phase)/self.frame_rate
        self.real_x -= self.horizontal_speed

    def vertical_move(self):
        self.rect.y = self.rect.y - self.angle_velocity * self.radius * cos(self.phase) / self.frame_rate

        self.phase += self.angle_velocity/self.frame_rate
        if self.phase > 2*pi:
            self.phase -= 2*pi
    def get_mask(self):
        return self.mask

    def get_rect(self):
        return self.rect
