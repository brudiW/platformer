import os
import pygame

class ModLoader:
    def __init__(self, game):
        self.game = game
        self.mods = []

    def load_mods(self):
        mod_folder = 'assets/mods'
        for filename in os.listdir(mod_folder):
            if filename.endswith('.py'):
                path = os.path.join(mod_folder, filename)
                with open(path) as f:
                    code = f.read()
                mod_globals = {
    				'game': self.game,
    				'register_hook': self.register_hook,
    				'register_item': register_item,
    				'ShopItem': ShopItem,
    				'CollectableItem': CollectableItem,
    				'OwnedItem': OwnedItem,
    				'pygame': pygame
				}
                exec(code, mod_globals)

    def register_hook(self, hook_func):
        self.mods.append(hook_func)
    
    def register_item(item):
	    game.items.add_item(item)

    def update(self):
        for hook in self.mods:
            hook()
