import os
import pygame

class ModLoader:
    def __init__(self, game):
        self.game = game
        self.mods = []

    def load_mods(self):
        mod_root = 'mods'
        for mod_name in os.listdir(mod_root):
            mod_path = os.path.join(mod_root, mod_name)
            if os.path.isdir(mod_path):
                mod_file = os.path.join(mod_path, 'mod.py')
                if os.path.isfile(mod_file):
                    with open(mod_file, 'r') as f:
                        code = f.read()
                    mod_globals = {
                        'game': self.game,
                        'register_hook': self.register_hook,
                        'register_item': lambda item: self.game.items.add_item(item),
                        'load_asset': lambda rel_path: pygame.image.load(os.path.join(mod_path, 'assets', rel_path)),
                        'pygame': pygame,
                        'ShopItem': ShopItem,
                        'CollectableItem': CollectableItem,
                        'OwnedItem': OwnedItem,
                    }
                    exec(code, mod_globals)

    def register_hook(self, hook_func):
        self.mods.append(hook_func)
    
    def register_item(self, item):
        self.game.items.add_item(item)

    def update(self):
        for hook in self.mods:
            hook()