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
        super().__init__(name, description, effect, texture, rarety)
        self.price = price
        
        
        
        
class CollectableItem(Item):
    def __init__(self, name, description, effect, texture, rarety):
        
        super().__init__(name, description, effect, texture, rarety)
    
    
class OwnedItem(Item):
    def __init__(self, name, description, effect, texture, rarety, durability):
        super().__init__(name, description, effect, texture, rarety)
        self.durability = durability
        
    def use(self):
        if not self.durability == -1 and self.durability > 0:
            self.durability -= 1