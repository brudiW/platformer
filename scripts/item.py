import pygame
import json

class Items:
    def __init__(self, game):
        self.game = game
        self.items = {}
        self.collectables = {}
        self.shop_items = {}
        self.owned_items = {}
        
    def add_item(self, item):
        if isinstance(item, ShopItem):
            self.shop_items[item.name] = item
        elif isinstance(item, CollectableItem):
            self.collectables[item.name] = item
        elif isinstance(item, OwnedItem):
            self.owned_items[item.name] = item
        else:
            raise ValueError("Invalid item type")
    def loadItems(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        self.itemlist = map_data['items']
        
        for item in self.itemlist.values():
            if item["type"] == "shop":
                self.add_item(ShopItem(item['name'], item['description'], item['effects'], item, item['rarety'], item['price']))
            elif item['type'] == 'collectable':
                self.add_item(CollectableItem(item['name'], item['description'], item['effects'], item, item['rarety']))
            elif item['type'] == 'owned':
                self.add_item(OwnedItem(item['name'], item['description'], item['effects'], item, item['rarety'], item['durability']))
class Item:
    def __init__(self, name, description, effect, texture, rarety):
        self.name = name
        self.description = description
        self.effect = effect
        self.texture = texture
        self.rarety = rarety

    def load_texture(self):
        if self.texture in self.game.assets:
            return self.game.assets[self.texture]
        else:
            raise ValueError(f"Texture {self.texture} not found in assets")
    
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
