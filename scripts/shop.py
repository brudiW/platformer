import pygame
import sys

class Shop:
    def __init__(self):
        self.shopItems = {}
    
    def addToShop(self, Item):
        self.shopItems.add(Item)