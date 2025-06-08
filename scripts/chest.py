import pygame

class Chest:
    def __init__(self, x, y, size, item):
        self.rect = pygame.Rect(x, y, size, size)
        self.item = item
        self.opened = False
