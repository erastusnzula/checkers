import pygame


class Settings:
    def __init__(self):
        self.width = self.height = 500
        self.bg_color = 245, 245, 245, 245
        self.icon = pygame.transform.scale(pygame.image.load('assets/images/icon.jpeg'), (50, 25))
        self.king_icon = pygame.transform.scale(pygame.image.load('assets/images/icon.jpeg'), (30, 25))

        self.rows = self.columns = 8
        self.size_width = self.width // self.columns
        self.size_height = self.width // self.columns
        self.white = 0, 0, 0, 0
        self.blue = 0, 0, 255, 255
        self.red = 200, 100, 100, 100
        self.grey = 128, 128, 128, 128
