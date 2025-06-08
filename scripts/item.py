import pygame
import json
import os

class ItemLoader:
    def __init__(self, game):
        self.game = game
        self.items = []

    def load_itemCode(self):
        item_root = 'hidden/items'
        for item_name in os.listdir(item_root):
            item_file = os.path.join(item_root, item_name)
            if os.path.isfile(item_file):
                with open(item_file, 'r') as f:
                    code = f.read()
                item_globals = {
                    'game': self.game,
                    'register_hook': self.register_hook,
                }
                exec(code, item_globals)

    def register_hook(self, hook_func):
        self.items.append(hook_func)

    def update(self):
        for hook in self.items:
            hook()

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
        for item_id, item_data in map_data.items():
            item_data["id"] = item_id  # Optional, um später auf die ID zuzugreifen

            if item_data["type"] == "shop":
                item_obj = ShopItem(
                    item_data['name'],
                    item_data['description'],
                    item_data['effects'],
                    "assets/images/items/" + item_data['texture'] + ".png",
                    item_data['rarety'],
                    item_data['price'],
                    self.game
                )
                self.shop_items[item_obj.name] = item_obj
            elif item_data['type'] == 'collectable':
                item_obj = CollectableItem(
                    item_data['name'],
                    item_data['description'],
                    item_data['effects'],
                    "assets/images/items/" + item_data['texture'] + ".png",
                    item_data['rarety'],
                    self.game
                )
                self.collectables[item_obj.name] = item_obj
            elif item_data['type'] == 'owned':
                item_obj = OwnedItem(
                    item_data['name'],
                    item_data['description'],
                    item_data['effects'],
                    "assets/images/items/" + item_data['texture'] + ".png",
                    item_data['rarety'],
                    item_data['durability'],
                    self.game
                )
                self.owned_items[item_obj.name] = item_obj
            self.items[item_id] = item_obj


    def list_items(self, sub):
        print("Items:")
        if sub == 'shop':
            for item in self.shop_items.values():
                print(f" - {item.name}: {item.description} (Price: {item.price})")
                self.showItem(item.texture)
        elif sub == 'collectable':
            for item in self.collectables.values():
                print(f" - {item.name}: {item.description}")
        elif sub == 'owned':
            for item in self.owned_items.values():
                print(f" - {item.name}: {item.description} (Durability: {item.durability})")
        else:
            print("Invalid category. Available categories: shop, collectable, owned")
            return
        print("All items:")
        for item in self.items.values():
            print(f" - {item.name}: {item.description}")

    def showItem(self, texture):
        return pygame.image.load(texture), (100, 100)
class Item:
    def __init__(self, name, description, effect, texture, rarety, game):
        self.name = name
        self.description = description
        self.effect = effect
        self.texture = texture
        self.rarety = rarety
        self.game = game
    

    def load_texture(self):
        return self.texture
        
    def getEffect(self):
        return self.effect
    
    def getItem(self):
        return {
            'name': self.name,
            'description': self.description,
            'effect': self.effect,
            'texture': self.texture,
            'rarety': self.rarety
        }
    
class ShopItem(Item):
    def __init__(self, name, description, effect, texture, rarety, price, game):
        super().__init__(name, description, effect, texture, rarety, game)
        self.price = price
        
        
        
        
class CollectableItem(Item):
    def __init__(self, name, description, effect, texture, rarety, game):
        
        super().__init__(name, description, effect, texture, rarety, game)
    
    
class OwnedItem(Item):
    def __init__(self, name, description, effect, texture, rarety, durability, game):
        super().__init__(name, description, effect, texture, rarety, game)
        self.durability = durability
        
    def use(self):
        if not self.durability == -1 and self.durability > 0:
            self.durability -= 1
    
    def equip(self, slot):
        if self.durability == 0:
            print("Item is broken")
            return False
        else:
            print("Item equipped")
            self.game.item_slots[slot] = self
            return True
            
