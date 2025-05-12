import pygame

class Item:
    def __init__(self, name, description, effect, texture, rarety):
        self.name = name
        self.description = description
        self.effect = effect
        self.texture = texture
        self.rarety = rarety
    
class ShopItem(Item):
    def __init__(self, name, description, effect, texture, rarety, price):
        super().init(name, description, effect, texture, rarety)
        self.price = price
        
        
        
        
class CollectableItem(Item):
    def __init__(self, name, description, effect, texture, rarety):
        
        super(name, description, effect, texture, rarety)
    
    
class OwnedItem(Item):
    def __init__(self, name, description, effect, texture, rarety, durability):
        
        self.durability = durability
        super(name, description, effect, texture, rarety)
        
    def use(self):
        if not self.durability == -1 and self.durability > 0:
            self.durability -= 1