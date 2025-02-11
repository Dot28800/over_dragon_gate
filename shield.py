import pygame
class Shield:
    def __init__(self, img_path,
                 screen_width=1600, screen_height=900,
                 x=1550,y=840,
                 size_x=20, size_y=60,
                 speed=10):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path).convert()
        self.img.set_colorkey((255, 255, 255))
        self.img = pygame.transform.scale(self.img, (size_x, size_y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = self.img.get_rect()
        self.size_x=size_x
        self.size_y=size_y
        self.rect.x =x
        self.rect.y = y
        self.real_x=self.screen_width
        self.horizontal_speed=speed
        self.vertical_speed=0
        self.gravity_acceleration=0.2
        self.invincible_duration=2000
        self.mask = pygame.mask.from_surface(self.img)
        self.visited=False
        self.collapsed=False
    def horizontal_move(self):
        self.rect.x -= self.horizontal_speed

    def vertical_move(self):
        self.vertical_speed += self.gravity_acceleration
        self.rect.y += self.vertical_speed
    def get_mask(self):
        return self.mask

    def get_rect(self):
        return self.rect