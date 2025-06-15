#Author: @SchimmelkellerCoding
#brudiW, Undertale  

import sys

import os

import pygame
from pygame._sdl2 import Window, Texture, Renderer

import json

import datetime

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.gamesave import GameSave
from scripts.item import Item, ShopItem, CollectableItem, OwnedItem, Items, ItemLoader
from scripts.modloader import ModLoader
from scripts.mainmenu import MainMenu
from scripts.button import Button
from scripts.levelselect import LevelSelect
from scripts.shop import Shop
from scripts.chest import Chest
from scripts.music import MusicPlayer
from scripts.notificationmanager import NotificationManager

class Game:
    def __init__(self):
        pygame.init()
        self.logtxt = [] # Initialisierung der Haupt-Logdatei
        self.logtxt.append(f"[INFO] Game started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Initializing Pygame and game components...")


        
        if pygame.get_init():
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Pygame initialized successfully")
        else:
            self.logtxt.append(f"[ERROR] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Pygame initialization failed")
            self.saveLog()  # Speichert Logdatei vor Beenden
            pygame.quit()
            sys.exit()
        

        if pygame.joystick.get_count() > 0: # Controller, falls vorhanden
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Controller detected")

            self.joy = pygame.joystick.Joystick(0)
            self.axlX = self.joy.get_axis(0) # laufen l = -1, r = 1
            self.axlY = self.joy.get_axis(1)
            self.axrX = self.joy.get_axis(2)
            self.axrY = self.joy.get_axis(3)
            self.leftBump = self.joy.get_axis(4)
            self.rightBump = self.joy.get_axis(5)
            self.btnA = self.joy.get_button(0) # springen
            self.startBTN = self.joy.get_button(7) # pause

            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Controller Name: {self.joy.get_name()}")
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Controller Axes: {self.joy.get_guid()}")
            self.logtxt.appendf("[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Controller initialized")
        else:
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] No controller detected")


        # Programm Fenster erstellung
        flags = pygame.RESIZABLE
        pygame.display.set_caption('Platformer')
        self.screen = pygame.display.set_mode((640, 480), flags)
        self.display = pygame.Surface((320, 240))
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Display initialized")

        self.mp = MusicPlayer() # Musik Player Initialisieren  

        self.notification_manager = NotificationManager(self)


        self.console_active = False
        self.console_input = ''
        self.console_output = []
        self.consolefont = pygame.font.Font(None, 24)
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Console initialized")

        self.clock = pygame.time.Clock() # Game Clock
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Clock initialized")
        
        self.items = Items(self) # Items Klasse laden
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Items initialized")
        
        #MODS INIT
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loading mods...")
        self.mod_loader = ModLoader(self)
        self.mod_loader.load_mods('assets/mods') # Mods laden

        if not len(self.mod_loader.mods) == 0:
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loaded {len(self.mod_loader.mods)} mods")
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loaded Mods: {self.mod_loader.mods}")
        else:
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] No mods found in assets/mods")
        
        print(self.mod_loader.mods) # // DEBUG
        print(self.mod_loader.commands) # // DEBUG 
        if not len(self.mod_loader.commands) == 0:
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loaded {len(self.mod_loader.commands)} mod commands")
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loaded Mod Commands: {self.mod_loader.commands}")
        else:
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] No mod commands found in mods")
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Mod loader initialized")


        #ITEMS INIT
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loading items...")
        self.item_loader = ItemLoader(self)
        self.item_loader.load_itemCode()
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Item loader initialized")

        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Initializing game components...")
        self.enemies = []
        self.physicsentities = []

        self.menu = MainMenu(self)

        self.items.loadItems('hidden/items.json') # Items aus hidden/items.json (Liste aller Items) laden
        self.items.list_items("owned")
        self.equipped_items = [] # Ausgerüstete Items
        self.item_slots = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
            "armor": None,
            "accessory": None
        }
        #for item in self.items.owned_items.values():
        #    item.equip("accessory")
        
        for itemslot in self.item_slots.values():
            print(f"{itemslot}")

        self.shop = Shop(self)
        self.shop.getShopItems()
        
        self.movement = [False, False] # links rechts bewegen

        self.tilemap = Tilemap(self, tile_size=16) # Map Laden
        
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loading Assets...")
        self.assets = { # Assets
            'grass': load_images('assets/images/tiles/grass'),
            'coin': load_images('assets/images/coin'),
            'player': load_image('assets/images/entities/Player.png'),
            'background': load_image(f"assets/images/background.png"),
            'decor': load_images('assets/images/decor'),
            'checkpoint': load_image('assets/images/checkpoint/checkpoint.png'),
            'mirror': load_image('assets/images/mirror/mirror.png'),
            'stone': load_images('assets/images/tiles/stone'),
            'enemy-1': load_image('assets/images/entities/enemy-1.png'),
            'fireball': load_image('assets/images/attacks/fireball.png'),
            'chest': load_images('assets/images/tiles/chest')
        }

        self.worldlist = [
            "1-1", "1-2"
        ]
        
        

        # Spielstand laden
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loading game save...")
        self.gamesave = GameSave()
        self.SAVE_PATH = 'hidden/worlds/save1.json'
        self.gamesave.updateLevel("1-2", {"unlocked": True,"completed": True, "time": 10}, self.SAVE_PATH) # // DEBUG
        #print(self.gamesave.getCoins(self.SAVE_PATH)) # // DEBUG


        
        

        self.scroll = [0, 0] # Kameraposition initialisieren
        
        self.jumps_left = 1  # Initialize jumps_left to allow double jumps
        self.run_speed = 0.5  # Zusätzliche Geschwindigkeit beim Rennen

        self.checkpoints = []
        self.mirrors = []
        self.coin_rects = []
        self.chests = []
        self.off_grid_coin_rects = [] # Rule 1: No Offgrid Coins

        self.player_lives = 3
        self.health_points = 6
        

        # Pause Initialization
        self.pause = False
        self.changePauseState = True

        # Main Menu Initialization
        self.inMainMenu = False

        self.energy = 100 # Energie, z.B. für Sprinten

        # Dynamically add checkpoints based on map data or predefined positions
        
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Initializing buttons and images...")
        self.resume_img = pygame.image.load("assets/images/button/button_resume.png").convert_alpha()
        self.restart_img = pygame.image.load('assets/images/button/button_back.png').convert_alpha()
        self.mainMenu_img = pygame.image.load("assets/images/button/button_quit.png").convert_alpha()

        self.resume_button = Button(104, 75, self.resume_img, 1)
        self.mainMenu_button = Button(136, 125, self.mainMenu_img, 1)
        self.restart_button = Button(132, 175, self.restart_img, 1)

        self.ls = LevelSelect(self, self.display)
        self.debugScreen = pygame.Surface((320, 240)) # Debug Screen
        self.debugState = False

        
        self.inWorld_ItemSelect("middle")

    def saveLog(self):
        """
        Speichert die Logdatei in hidden/logs/latest.log
        """
        with open('hidden/logs/latest.log', 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.logtxt))

        now = datetime.datetime.now()
        filename = now.strftime("hidden/logs/log_%Y-%m-%d_%H-%M-%S.log")
        with open(filename, "w", encoding="utf-8") as f:
            f.write('\n'.join(self.logtxt))
        print("[INFO] Log saved to hidden/logs/latest.log and " + filename)

    def loadWorld(self, path: str):
        """Lädt die Level-Tilemap aus dem angegebenen Pfad.

        Args:
            path (str): Der Pfad, aus dem die Level-Tilemap geladen.
        """
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Loading world from {path}")
        self.tilemap.load(path)

        self.spawn_location = (self.tilemap.playerSpawn())  # Default spawn location

        self.player = Player(self, (self.tilemap.playerSpawn()[0], self.tilemap.playerSpawn()[1]), (5, 13)) # Player Erstellen
        self.enemyA = Enemy(self, "enemy-1", (300, 60), (16, 16), 'fireball', 3)
        self.enemies.append(self.enemyA)
        self.physicsentities.append(self.player)
        self.physicsentities.append(self.enemyA)

        for tile in self.tilemap.tilemap.values(): # Adding Effect Tiles
            if tile['type'] == 'checkpoint':
                checkpoint_rect = pygame.Rect(tile['pos'][0] * self.tilemap.tile_size, tile['pos'][1] * self.tilemap.tile_size, self.tilemap.tile_size, self.tilemap.tile_size)
                self.checkpoints.append(checkpoint_rect)
            if tile['type'] == 'mirror':
                mirror_rect = pygame.Rect(tile['pos'][0] * self.tilemap.tile_size, tile['pos'][1] * self.tilemap.tile_size, self.tilemap.tile_size, self.tilemap.tile_size)
                self.mirrors.append(mirror_rect)
            if tile['type'] == 'coin': 
                coin_rect = pygame.Rect(tile['pos'][0] * self.tilemap.tile_size, tile['pos'][1] * self.tilemap.tile_size, self.tilemap.tile_size, self.tilemap.tile_size)
                self.coin_rects.append(coin_rect)
            if tile['type'] == 'chest':
                x = tile['pos'][0] * self.tilemap.tile_size
                y = tile['pos'][1] * self.tilemap.tile_size
                item = tile.get('item')
                chest_obj = Chest(x, y, self.tilemap.tile_size, item)
                self.chests.append(chest_obj)
        for tile in self.tilemap.offgrid_tiles: # RUle 1: No Offgrid Coins
            if tile['type'] == 'coin':
                coin_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], self.tilemap.tile_size, self.tilemap.tile_size)
                self.off_grid_coin_rects.append(coin_rect)

    def unloadWorld(self):
        """Entlädt die Level-Tilemap um keine Probleme beim Laden eines anderen Levels zu verursachen.
        """
        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Unloading current world")
        self.enemies = []
        self.physicsentities = []

        self.checkpoints = []
        self.mirrors = []
        self.coin_rects = []
        self.off_grid_coin_rects = [] # Rule 1: No Offgrid Coins

    def collectChestContents(self, chest: dict):
        """Liest den Inhalt einer Kiste aus und gibt das enthaltene Item dem Spieler ins Inventar.

        Args:
            chest (dict): Die Kiste
        """
        item_id = getattr(chest, 'item', None)
        if item_id:
            print(f"Alle Items: {self.items.items.items()}")
            item_obj = self.items.items.get(item_id)
            print(f"Gefundenes Item: {item_obj}")
            if item_obj:
                self.items.owned_items[item_id] = item_obj
                print(f"Item gesammelt (ID: {item_id}): {getattr(item_obj, 'name', 'Unbenannt')}")
                self.gamesave.addItem(item_id, item_obj, self.SAVE_PATH)  # Speichere Item im Spielstand
                if item_id == "schal_der_leichtigkeit":
                    self.notification_manager.add_notification("Doppelsprung freigeschaltet!")
                    self.mp.play_sound('assets/sounds/item-collect.mp3')
            else:
                print(f"Unbekannte Item-ID: {item_id}")




    def inWorld_ItemSelect(self, itemslot: str):
        """Legt den ausgewählten Item-Slot fest

        Args:
            itemslot (str): Der ausgewählte Item-Slot
        """
        self.selected_itemslot = itemslot  # Speichere Auswahl zur Anzeige später
        
    def execute_command(self, command: str):
        """Liest die Eingabe aus der Konsole ein und führt den Befehl aus
        Wenn der Befehl erfolgreich ausgeführt wurde, wird eine Nachricht der Konsolenausgabe angefügt.

        Args:
            command (str): Der auszuführende Befehl
        """
        try:
            parts = command.strip().split()
            if not parts:
                return
            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Executing command: {command}")
            
            cmd = parts[0]
            args = parts[1:]
            if cmd == "set_energy" and len(args) == 1:
                value = int(args[0])
                self.energy = value
                self.console_output.append(f"Energy set to {value}")
                self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Energy set to {value}")
            elif (cmd == "teleport" or cmd == "tp") and len(args) == 2:
                x, y = map(int, args)
                self.player.pos = [x, y]
                self.console_output.append(f"Teleported to {x}, {y}")
                self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Teleported player to {x}, {y}")
            elif cmd == "godmode":
                self.health_points = 999
                self.player_lives = 999
                self.console_output.append("Godmode activated")
                self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Godmode activated")
            elif cmd == "list" and len(args) == 1:
                sub = args[0]
                if sub == 'enemy':
                    for enemy in self.enemies:
                        self.console_output.append(f"Enemy: {enemy.type} at {enemy.pos}")
                        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Listed enemy: {enemy.type} at {enemy.pos}")
                elif sub == 'checkpoint':
                    for checkpoint in self.checkpoints:
                        self.console_output.append(f"Checkpoint: {checkpoint}")
                        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Listed checkpoint: {checkpoint}")
                elif sub == 'coin':
                    for coin in self.coin_rects:
                        self.console_output.append(f"Coin: {coin}")
                        self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Listed coin: {coin}")
            
            elif cmd == "coin" and len(args) == 2:
                sub = args[0]
                end = args[1]
                if sub == 'give':
                    self.gamesave.updateCoins(self.SAVE_PATH, int(self.gamesave.getCoins(self.SAVE_PATH) + int(end)))
                    self.console_output.append(f"Added {end} coins")
                    self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Added {end} coins to save")
                elif sub == 'remove':
                    self.gamesave.updateCoins(self.SAVE_PATH, int(self.gamesave.getCoins(self.SAVE_PATH) - int(end)))
                    self.console_output.append(f"Removed {end} coins")
                    self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Removed {end} coins from save")
                    
            elif cmd == "coin" and len(args) == 1:
                sub = args[0]
                if sub == 'list':
                    self.console_output.append(f"Coins: {self.gamesave.getCoins(self.SAVE_PATH)}")
                    self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Listed coins: {self.gamesave.getCoins(self.SAVE_PATH)}")
            elif cmd == "debug":
                self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Toggling debug window")
                if not self.debugState:
                    
                    self.setup_debug_window()  # Debug Window Setup
                else:
                    self.debug_window.destroy()
                self.debugState = not self.debugState
                

            elif cmd == "mods":
                for mod in self.mod_loader.get_mod_list():
                    self.console_output.append(f"Mod: {mod['name']} by {mod['author']} - {mod['description']}")
                    self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Listed mod: {mod['name']} by {mod['author']} - {mod['description']}")

            elif cmd == "stop" or cmd == "crash":
                self.save_console_logs()  # Speichert Logs vor Beenden
                self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Game stopped by user command")
                self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Stopping game")
                self.logtxt.append(f"[INFO] Game ended at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.saveLog()
                pygame.quit()
                sys.exit()

            elif cmd == "help" and len(args) == 1:
                sub = args[0]
                match sub:
                    case "set_energy":
                        self.console_output.append("set_energy <val>\nSets the energy level.")
                    case "teleport" | "tp":
                        self.console_output.append("teleport <x> <y>\nMoves the player to those coordinates.")
                    case "godmode":
                        self.console_output.append("Enables godmode")
                    case "coin":
                        self.console_output.append("coin [give|remove] <val>\nGives/removes coins.\ncoin list\nReturns the amount of coins.")
                    case "list":
                        self.console_output.append("list [enemy|checkpoints|cp|coin]\nLists all enemys, checkpoints or coins in the map.")
                    case "debug":
                        self.console_output.append("Opens/Closes the debug window")
                    case "stop" | "crash":
                        self.console_output.append("Closes the game.")
                    case "mods":
                        self.console_output.append("Lists all mods.")
                    case "help":
                        self.console_output.append("Do you really need this much help?!")
                
            elif cmd == "help":
                self.console_output.append("Commands: set_energy <val>, teleport <x> <y>, godmode, coin [give|remove] <val>, coin [list], list [enemy|checkpoints|cp|coin], debug, stop, crash, help")
                if hasattr(self.mod_loader, "commands"):
                    self.console_output.append("Mod Commands: " + ", ".join(self.mod_loader.commands.keys()))
                elif hasattr(self.mod_loader, "commands") and cmd in self.mod_loader.commands:
                    result = self.mod_loader.run_command(cmd, *args)
                    if result is not None:
                        self.console_output.append(str(result))
                    else:
                        self.console_output.append(f"Executed mod command: {cmd}")
            elif cmd in self.mod_loader.commands:
                result = self.mod_loader.run_command(cmd, *args)
                if result is not None:
                    self.console_output.append(str(result))
                else:
                    self.console_output.append(f"Executed mod command: {cmd}")
            else:
                self.console_output.append("Unknown command.")
        except Exception as e:
            self.console_output.append(f"Error: {str(e)}")
            self.logtxt.append(f"[ERROR] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Command execution failed: {str(e)}")

    def reset(self):
        """Setzt einige game Variablen zurück
        """
        # Reset game state
        self.player = Player(self, (self.tilemap.playerSpawn()[0], self.tilemap.playerSpawn()[1]), (5, 13))
        self.enemies.clear()
        self.physicsentities.clear()
        self.scroll = [0, 0]
        self.jumps_left = 1
        self.run_speed = 0.5
        self.player_lives = 3
        self.health_points = 6
        self.energy = 100
        self.spawn_location = (self.tilemap.playerSpawn())
        
        # Reinitialize enemies and physics entities
        self.enemyA = Enemy(self, "enemy-1", (300, 60), (16, 16), 'fireball', 3)
        self.enemies.append(self.enemyA)
        self.physicsentities.append(self.player)
        self.physicsentities.append(self.enemyA)

    def setup_debug_window(self):
        """Bereitet das Debug-Fenster vor
        """
        self.debug_window = Window("Debug Info", size=(400, 300), position=(50, 50))
        self.debug_renderer = Renderer(self.debug_window)


    def debug(self):
        """Aktualisiert das Debug-Fenster
        """
        # Debug-Surface leeren (schwarz füllen)
        self.debugScreen.fill((0, 0, 0))

        font = pygame.font.Font(None, 18)

        # Debug-Infos in Zeilen speichern
        lines = [
            f"Player Pos: {self.player.pos}",
            f"Lives: {self.player_lives}",
            f"Health: {self.health_points}",
            f"Energy: {int(self.energy)}",
            f"FPS: {int(self.clock.get_fps())}",
            f"Mouse Pos: {pygame.mouse.get_pos()}",
            f"Selected Slot: {getattr(self, 'selected_itemslot', 'None')}"
        ]

        # Zeilen rendern & auf Surface blitten
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            self.debugScreen.blit(text_surface, (10, 10 + i * 20))

        # Surface zu Texture & anzeigen
        debug_texture = pygame._sdl2.Texture.from_surface(self.debug_renderer, self.debugScreen)
        self.debug_renderer.clear()
        debug_texture.draw()
        self.debug_renderer.present()

    
    def save_console_logs(self):
        """Speichert den Inhalt der Ingame-Konsole in hidden/latest.log
        """
        # Inhalt aus console_output in String zusammenfügen
        log_text = "\n".join(self.console_output)

        # 1. Datei: latest.log (überschreiben)
        with open("hidden/latest.log", "w", encoding="utf-8") as f:
            f.write(log_text)

        # 2. Datei: Datum + Uhrzeit als Dateiname
        now = datetime.datetime.now()
        filename = now.strftime("hidden/log_%Y-%m-%d_%H-%M-%S.log")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(log_text)

        print(f"[INFO] Logs gespeichert: latest.log und {filename}")



    
    def run(self):
        """MAIN GAME LOOP
        """
        #Main Game Loop
        self.mainstate = "start"
        while True:
            if self.mainstate == "select":
                self.ls.run()
                self.screen.blit(pygame.transform.scale(self.ls.display, self.screen.get_size()), (0, 0))
                pygame.display.set_caption('Platformer')
                pygame.display.update()
                self.clock.tick(60)
            if self.mainstate == "start":
                self.menu.showMainMenu()
                pygame.display.set_caption("MAIN MENU")
                pygame.display.update()
            # if self.mainstate == "shop":
            #     self.shop.showShop(self.display)
                #self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                #pygame.display.update()
                #self.clock.tick(60)
            if self.mainstate == "game":
                if not self.pause:
                    self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                    self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                    render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                    self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.mod_loader.update() # MODS // SPÄTER WIEDER EINBAUEN
                    self.item_loader.update() # ITEMS
                    # falls Controller vorhanden
                    if pygame.joystick.get_count() > 0:
                        self.axlX = self.joy.get_axis(0) # laufen l = -1, r = 1
                        self.axlY = self.joy.get_axis(1)
                        self.axrX = self.joy.get_axis(2)
                        self.axrY = self.joy.get_axis(3)
                        self.leftBump = self.joy.get_axis(4)
                        self.rightBump = self.joy.get_axis(5)
                        self.btnA = self.joy.get_button(0) # springen
                        self.startBTN = self.joy.get_button(7) # pause
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.save_console_logs()
                            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Stopping game")
                            self.logtxt.append(f"[INFO] Game ended at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            self.saveLog()
                            pygame.quit()
                            sys.exit()


                        # Controller
                        if pygame.joystick.get_count() > 0:
                            if not self.pause:
                                if self.axlX > 0.1:
                                    self.movement[1] = True
                                    self.movement[0] = False
                                if self.axlX < -0.1:
                                    self.movement[0] = True
                                    self.movement[1] = False
                                if -0.1 < self.axlX and self.axlX < 0.1:
                                    self.movement[0], self.movement[1] = False, False
                                if self.btnA > 0.5: # JUMP
                                    if self.jumps_left > 0:
                                        self.player.velocity[1] = -2.7
                                        self.jumps_left -= 1

                                if self.rightBump > 0 and self.energy > 0:
                                    self.energy -= 0.1
                                    self.run_speed = 1.5  # Erhöhe die Geschwindigkeit beim Rennen
                                if self.rightBump < 0 or self.energy <= 0:
                                    self.run_speed = 0.5  # Setze die Geschwindigkeit zurück

                                if self.axrX < -0.7:
                                    if self.axrY > -0.7 and self.axrY < 0.7:
                                        print("Links")
                                        self.inWorld_ItemSelect("left")
                                elif self.axrX > 0.7:
                                    if self.axrY > -0.7 and self.axrY < 0.7:
                                        print("Rechts")
                                        self.inWorld_ItemSelect("right")
                                elif self.axrX > -0.7 and self.axlX < 0.7:
                                    if self.axrY > 0.7:
                                        print("Unten")
                                        self.inWorld_ItemSelect("bottom")
                                    elif self.axrY < -0.7:
                                        print("Oben")
                                        self.inWorld_ItemSelect("top")
                                    elif self.axrY > -0.7 and self.axrY < 0.7:
                                        self.inWorld_ItemSelect("middle")
                                        pass
                                #print(f"Right Stick X: {self.axrX}, Right Stick Y: {self.axrY}")

                            if self.startBTN > 0.5 and not self.pause:
                                if self.changePauseState:
                                    self.pause = True
                                    print(self.pause)
                                    self.changePauseState = False
                            elif self.startBTN > 0.5 and self.pause:
                                if self.changePauseState:
                                    self.pause = False
                                    print(self.pause)
                                    self.changePauseState = False
                            if self.startBTN < 0.5:
                                self.changePauseState = True

                        # Keyboard
                        if event.type == pygame.KEYDOWN:
                            if not self.pause:
                                if event.key == pygame.K_LEFT:  # MOVE LEFT
                                    self.movement[0] = True
                                if event.key == pygame.K_RIGHT:  # MOVE RIGHT
                                    self.movement[1] = True
                                if event.key == pygame.K_SPACE:  # JUMP
                                    if self.jumps_left > 0:
                                        self.player.velocity[1] = -2.7
                                        self.jumps_left -= 1
                                        self.mp.play_sound("assets/sounds/Jump.mp3")  # Sound beim Springen abspielen
                                if event.key == pygame.K_LSHIFT and self.energy > 0:  # RUN
                                    self.energy -= 0.1
                                    self.run_speed = 1.5  # Erhöhe die Geschwindigkeit beim Rennen
                            if event.key == pygame.K_ESCAPE and not self.pause:
                                if self.changePauseState:
                                    self.pause = True
                                    print(self.pause)
                                    self.changePauseState = False
                            if event.key == pygame.K_ESCAPE and self.pause:
                                if self.changePauseState:
                                    self.pause = False
                                    print(self.pause)
                                    self.changePauseState = False

                            if event.key == pygame.K_TAB: #s and event.key == pygame.K_t and (event.key == pygame.K_KP_DIVIDE or event.key == pygame.K_SLASH):
                                self.console_active = not self.console_active  # Toggle console

                            if self.console_active:
                                if event.key == pygame.K_BACKSPACE:
                                    self.console_input = self.console_input[:-1]
                                elif event.key == pygame.K_RETURN:
                                    self.console_output.append("> " + self.console_input)
                                    self.execute_command(self.console_input)
                                    self.console_input = ''
                                else:
                                    self.console_input += event.unicode

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_LEFT:
                                self.movement[0] = False
                            if event.key == pygame.K_RIGHT:
                                self.movement[1] = False
                            if event.key == pygame.K_LSHIFT:  # STOP RUNNING
                                self.run_speed = 0.5  # Setze die Geschwindigkeit zurück
                            if event.key == pygame.K_ESCAPE:
                                self.changePauseState = True
                        if self.energy <= 0:
                            self.run_speed = 0.5

                    if not self.pause:
                        if os.path.exists(self.SAVE_PATH):
                            for level in self.worldlist:
                                self.gamesave.checkUnlock(level, self.SAVE_PATH)
                        else:
                            print(f"[WARNING] Speicherdatei nicht gefunden: {self.SAVE_PATH}")
                            self.logtxt.append(f"[WARNING] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Speicherdatei nicht gefunden: {self.SAVE_PATH}")

                        self.display.blit(load_image(f"assets/images/{self.tilemap.getBackground()}.png"), (0, 0))

                        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                        self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))

                        self.tilemap.render(self.display, offset=render_scroll)


                        self.player.render(self.display, offset=render_scroll)
                        for enemy in self.enemies:
                            enemy.update(self.tilemap, (0, 0))
                            enemy.render(self.display, offset=render_scroll)
                            if self.player.rect().colliderect(enemy.rect()):
                                player_rect = self.player.rect()
                                enemy_rect = enemy.rect()


                                # Berechne die Kollision von jeder Seite
                                if player_rect.bottom > enemy_rect.top and player_rect.top < enemy_rect.top:
                                    # Spieler trifft den Gegner von oben – kein Schaden
                                    self.enemies.remove(enemy)
                                else:
                                    # Schaden nur bei Kollision von links, rechts oder unten
                                    self.health_points -= 5
                                    self.mp.play_sound("assets/sounds/Hurt.mp3")  # Sound bei Schaden abspielen



                        self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * self.run_speed, 0))

                        if self.player.collisions['down']:
                            self.jumps_left = 1  # Reset jumps_left when the player lands

                        if self.player.rect().y > self.display.get_height() + 50:
                            self.mp.play_sound("assets/sounds/Hurt.mp3")  # Sound beim Tod abspielen
                            self.player_lives -= 1
                            if self.player_lives > 0:
                                self.player.pos[0], self.player.pos[1] = self.spawn_location[0], self.spawn_location[1] - 2
                            else:
                                t = pygame.time.get_ticks()
                                print(t/1000)
                                self.unloadWorld()
                                self.reset()
                                self.ls.reset()
                                self.mainstate = "select"
                                self.mp.play("assets/sounds/Overworld.mp3", loop=True)  # Sound beim Tod abspielen

                        if self.health_points <= 0:
                            self.player_lives -= 1
                            self.health_points = 6
                            if self.player_lives > 0:
                                self.player.pos[0], self.player.pos[1] = self.spawn_location[0], self.spawn_location[1] - 2
                            else:
                                t = pygame.time.get_ticks()
                                print(t/1000)
                                self.unloadWorld()
                                self.reset()
                                self.ls.reset()
                                self.mainstate = "select"
                                self.mp.play("assets/sounds/Overworld.mp3", loop=True)  # Sound beim Tod abspielen

                        life_text = pygame.font.Font.render(pygame.font.Font(None, 24), f"Lives: {self.player_lives}", True, (255, 255, 255))
                        #energy_text = pygame.font.Font.render(pygame.font.Font(None, 24), f"Energy: {int(self.energy)}", True, (255, 255, 255))
                        #mousetext = pygame.font.Font.render(pygame.font.Font(None, 12), f"Mouse Position: {pygame.mouse.get_pos()}, Mouse Buttons: {pygame.mouse.get_pressed(5)}", True, (255, 255, 255))
                        self.display.blit(life_text, (10, 10))
                        #self.display.blit(energy_text, (10, 30))
                        #self.display.blit(mousetext, (10, 50))
                        if hasattr(self, 'selected_itemslot') and not self.selected_itemslot == "middle":
                            pygame.draw.circle(self.display, (255, 255, 0), (self.display.get_width() // 2, self.display.get_height() // 2), 40, 20)
                        #self.enemyA.attack(self.player.pos, 'fireball', offset=render_scroll)
                        #for entity in self.physicsentities:
                        #    entity.drawHitbox(self.display, offset=render_scroll)


                        #self.display.blit(pygame.image.load("assets/images/items/schal_der_leichtigkeit.png"), (100, 100))
                        if self.console_active:
                            pygame.draw.rect(self.display, (0, 0, 0), (0, self.display.get_height() - 60, self.display.get_width(), 60))
                            input_surface = self.consolefont.render(self.console_input, True, (0, 255, 0))
                            self.display.blit(input_surface, (10, self.display.get_height() - 50))

                            for i, line in enumerate(self.console_output[-2:]):  # Show last 2 lines
                                output_surface = self.consolefont.render(line, True, (255, 255, 255))
                                self.display.blit(output_surface, (10, self.display.get_height() - 70 - (20 * i)))

                        


                        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                        self.notification_manager.update()
                        self.notification_manager.draw()
                        pygame.display.set_caption('Platformer')
                        pygame.display.update()
                        self.clock.tick(60)
                if self.pause: # PAUSE MENU
                    # Vorher im Code (z. B. im Game-Loop)
                    mouse_clicked = False

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.save_console_logs()
                            self.logtxt.append(f"[INFO] [{datetime.datetime.now().strftime('%H:%M:%S.%f')}] Stopping game")
                            self.logtxt.append(f"[INFO] Game ended at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            self.saveLog()
                            pygame.quit()
                            sys.exit()

                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                if self.changePauseState:
                                    self.pause = not self.pause
                                    print(f"[DEBUG] Pause toggled: {self.pause}")
                                    self.changePauseState = False

                        elif event.type == pygame.KEYUP:
                            if event.key == pygame.K_ESCAPE:
                                self.changePauseState = True

                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mouse_clicked = True

                    pygame.display.set_caption('Platformer (Paused)')
                    font = pygame.font.Font(None, 36)
                    small_font = pygame.font.Font(None, 24)

                    text = font.render("Paused", True, (255, 255, 255))
                    continue_text = small_font.render("CONTINUE", True, (255, 255, 255))
                    restart_text = small_font.render("RESTART", True, (255, 255, 255))
                    main_menu_text = small_font.render("MAIN MENU", True, (255, 255, 255))

                    # Positionen berechnen
                    cx = self.display.get_width() // 2
                    y_base = self.display.get_height() // 2 - self.display.get_height() // 4

                    # Buttons zeichnen
                    rect_continue = pygame.Rect(cx - 100, y_base + 60, 200, 40)
                    rect_restart = pygame.Rect(cx - 100, y_base + 110, 200, 40)
                    rect_main_menu = pygame.Rect(cx - 100, y_base + 160, 200, 40)

                    pygame.draw.rect(self.display, (190, 0, 0), rect_continue, border_radius=10)
                    pygame.draw.rect(self.display, (0, 190, 0), rect_restart, border_radius=10)
                    pygame.draw.rect(self.display, (0, 0, 190), rect_main_menu, border_radius=10)

                    # Texte zeichnen
                    self.display.blit(text, (cx - text.get_width() // 2, y_base))
                    self.display.blit(continue_text, (cx - continue_text.get_width() // 2, rect_continue.y + 5))
                    self.display.blit(restart_text, (cx - restart_text.get_width() // 2, rect_restart.y + 5))
                    self.display.blit(main_menu_text, (cx - main_menu_text.get_width() // 2, rect_main_menu.y + 5))

                    # Skaliertes Display auf Bildschirm
                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

                    # Button-Klicks abfangen
                    if mouse_clicked:
                        mouse_pos = pygame.mouse.get_pos()
                        scaled_mouse = (mouse_pos[0] * self.display.get_width() / self.screen.get_width(),
                        mouse_pos[1] * self.display.get_height() / self.screen.get_height())

                        if rect_continue.collidepoint(scaled_mouse):
                            self.pause = False
                            self.changePauseState = True

                        elif rect_restart.collidepoint(scaled_mouse):
                            self.reset()
                            self.pause = False
                            self.changePauseState = True

                        elif rect_main_menu.collidepoint(scaled_mouse):
                            self.reset()
                            self.mainstate = "start"
                            self.inMainMenu = True
                            self.pause = False
                            self.changePauseState = True
                            self.mp.play("assets/sounds/Overworld.mp3", loop=True)  # Sound beim Wechsel zum Hauptmenü abspielen

                    
                    pygame.display.update()
                    self.clock.tick(60)
            if self.debugState:
                # Zeichne Debug-Infos auf debugScreen (Surface)
                self.debug()
