import random

import pygame


class Needle_trap:
    def __init__(self, img_path,
                 screen_width=1600, screen_height=900,
                 size_x=20, size_y=60,
                 upper_bound=0,lower_bound=0,
                 horizontal_speed=10,vertical_speed=3,frame_rate=50):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path).convert()
        self.img.set_colorkey((255, 255, 255))
        self.img = pygame.transform.scale(self.img, (size_x, size_y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = self.img.get_rect()
        self.size_x=size_x
        self.size_y=size_y
        self.rect.x =self.screen_width
        self.upper_bound=upper_bound
        self.lower_bound=lower_bound
        self.rect.y = random.randint(self.upper_bound,self.lower_bound)
        self.horizontal_speed=horizontal_speed
        self.real_x=self.rect.x
        self.vertical_speed=vertical_speed
        self.frame_rate=frame_rate
        self.mask = pygame.mask.from_surface(self.img)
        self.visited=False
        self.collapsed=False
        self.downward=True

    def horizontal_move(self):
        self.rect.x -= self.horizontal_speed

    def vertical_move(self):
        if self.downward:
            self.rect.y=min(self.rect.y+self.vertical_speed,self.lower_bound)
            if self.rect.y>=self.lower_bound:
                self.downward=False
        else:
            self.rect.y=max(self.rect.y-self.vertical_speed,self.upper_bound)
            if self.rect.y<=self.upper_bound:
                self.downward=True

    def get_mask(self):
        return self.mask

    def get_rect(self):
        return self.rect

