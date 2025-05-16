import os

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
                }
                exec(code, mod_globals)

    def register_hook(self, hook_func):
        self.mods.append(hook_func)

    def update(self):
        for hook in self.mods:
            hook()