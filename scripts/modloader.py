import os
import pygame
from scripts.item import ShopItem, CollectableItem, OwnedItem

class ModLoader:
    def __init__(self, game):
        self.game = game
        self.mods = []
        self.modlist = []
        self.commands = {}  # Store command name -> function

    def load_mods(self, path: str):
        """
        Lädt alle Mods aus dem angegebenen Verzeichnis.
        Args:
            path (str): Der Pfad zum Verzeichnis, das die Mods enthält.
        """
        mod_root = path
        for mod_name in os.listdir(mod_root):
            mod_path = os.path.join(mod_root, mod_name)
            if os.path.isdir(mod_path):
                mod_file = os.path.join(mod_path, 'mod.py')
                if os.path.isfile(mod_file):
                    with open(mod_file, 'r') as f:
                        code = f.read()
                    mod_globals = {
                        'game': self.game,
                        'register_mod': self.register_mod,
                        'register_hook': self.register_hook,
                        'register_item': lambda item: self.game.items.add_item(item),
                        'register_command': self.register_command,
                        'load_asset': lambda rel_path: pygame.image.load(os.path.join(mod_path, 'assets', rel_path)),
                        'pygame': pygame,
                        'ShopItem': ShopItem,
                        'CollectableItem': CollectableItem,
                        'OwnedItem': OwnedItem,
                    }
                    exec(code, mod_globals)

    def register_mod(self, mod_name: str, mod_description: str, mod_author: str):
        """ Registriert einen Mod mit den angegebenen Informationen.
        Args:
            mod_name (str): Der Name des Mods.
            mod_description (str): Eine kurze Beschreibung des Mods.
            mod_author (str): Der Autor des Mods.
        """
        mod_info = {
            'name': mod_name,
            'description': mod_description,
            'author': mod_author
        }
        self.modlist.append(mod_info)
        print(f"Mod '{mod_name}' by {mod_author} registered.")

    def get_mod_list(self):
        """ Gibt eine Liste aller geladenen Mods zurück.
        Returns:
            list: Eine Liste von Dictionaries, die Informationen über die Mods enthalten.
        """
        if len(self.modlist) == 0:
            return "No mods loaded." # Mögliche Fehlerstelle, wenn keine Mods vorhanden
        else:
            return self.modlist

    def register_hook(self, hook_func):
        """ Registriert eine Hook-Funktion, die in jedem Update-Zyklus aufgerufen wird.
        Args:
            hook_func (function): Die Funktion, die als Hook registriert werden soll.
        """
        self.mods.append(hook_func)
    
    def register_command(self, name: str, func):
        """ Registriert einen Befehl, der später ausgeführt werden kann.
        Args:
            name (str): Der Name des Befehls.
            func (function): Die Funktion, die ausgeführt wird, wenn der Befehl aufgerufen wird.
        """
        self.commands[name] = func

    def run_command(self, name: str, *args, **kwargs):
        """ Führt einen registrierten Befehl aus.
        Args:
            name (str): Der Name des Befehls.
            *args: Zusätzliche Argumente, die an den Befehl übergeben werden.
            **kwargs: Zusätzliche Schlüsselwortargumente, die an den Befehl übergeben werden.

        Returns:
            Das Ergebnis der Befehlsfunktion, falls vorhanden.
        """
        if name in self.commands:
            return self.commands[name](*args, **kwargs)
        else:
            print(f"Command '{name}' not found.")

    def update(self):
        """ Führt alle registrierten Hook-Funktionen aus. """
        for hook in self.mods:
            hook()
