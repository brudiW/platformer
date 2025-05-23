import sys

import os

import pygame

import json

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.gamesave import GameSave
from scripts.item import Item, ShopItem, CollectableItem, OwnedItem, Items, ItemLoader
from scripts.modloader import ModLoader
from scripts.mainmenu import MainMenu
from scripts.button import Button

class Game:
    def __init__(self):
        pygame.init()
        if pygame.joystick.get_count() > 0: # Controller, falls vorhanden
            self.joy = pygame.joystick.Joystick(0)
            self.axlX = self.joy.get_axis(0) # laufen l = -1, r = 1
            self.axlY = self.joy.get_axis(1)
            self.axrX = self.joy.get_axis(2)
            self.axrY = self.joy.get_axis(3)
            self.leftBump = self.joy.get_axis(4)
            self.rightBump = self.joy.get_axis(5)
            self.btnA = self.joy.get_button(0) # springen
            self.startBTN = self.joy.get_button(7) # pause
        
        
        

        # Programm Fenster erstellung
        pygame.display.set_caption('Platformer')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.console_active = False
        self.console_input = ''
        self.console_output = []
        self.consolefont = pygame.font.Font(None, 24)


        self.clock = pygame.time.Clock() # Game Clock
        
        self.items = Items(self) # Items Klasse laden
        
        self.mod_loader = ModLoader(self)
        self.mod_loader.load_mods('assets/mods') # Mods laden
        print(self.mod_loader.mods) # // DEBUG
        print(self.mod_loader.commands) # // DEBUG 
        self.item_loader = ItemLoader(self)
        self.item_loader.load_itemCode()

        self.enemies = []
        self.physicsentities = []

        self.menu = MainMenu(self)

        self.items.loadItems('hidden/items.json') # Items aus hidden/items.json (Liste aller Items) laden
        self.items.list_items("owned")
        self.equpped_items = [] # Ausgerüstete Items
        self.item_slots = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
            "armor": None,
            "accessory": None
        }
        for item in self.items.owned_items.values():
            item.equip("accessory")
        
        for itemslot in self.item_slots.values():
            print(f"{itemslot}")
        
        self.movement = [False, False] # links rechts bewegen

        self.tilemap = Tilemap(self, tile_size=16) # Map Laden
        
        self.assets = { # Assets
            'grass': load_images('images/tiles/grass'),
            'coin': load_images('images/coin'),
            'player': load_image('images/entities/Player.png'),
            'background': load_image(f"images/{self.tilemap.getBackground()}.png"),
            'decor': load_images('images/decor'),
            'checkpoint': load_image('images/checkpoint/checkpoint.png'),
            'mirror': load_image('images/mirror/mirror.png'),
            'stone': load_images('images/tiles/stone'),
            'enemy-1': load_image('images/entities/enemy-1.png'),
            'fireball': load_image('images/attacks/fireball.png')
        }

        self.worldlist = [
            "1-1", "1-2"
        ]
        
        self.tilemap.load('assets/maps/1-1.json')

        # Spielstand laden
        self.gamesave = GameSave()
        self.SAVE_PATH = 'hidden/worlds/save1.json'
        self.gamesave.updateLevel("1-2", {"unlocked": True,"completed": True, "time": 10}, self.SAVE_PATH) # // DEBUG
        print(self.gamesave.getCoins(self.SAVE_PATH)) # // DEBUG


        self.player = Player(self, (self.tilemap.playerSpawn()[0], self.tilemap.playerSpawn()[1]), (5, 13)) # Player Erstellen
        self.enemyA = Enemy(self, "enemy-1", (300, 60), (16, 16), 'fireball', 3)
        self.enemies.append(self.enemyA)
        self.physicsentities.append(self.player)
        self.physicsentities.append(self.enemyA)

        self.scroll = [0, 0] # Kameraposition initialisieren
        
        self.jumps_left = 1  # Initialize jumps_left to allow double jumps
        self.run_speed = 0.5  # Zusätzliche Geschwindigkeit beim Rennen

        self.checkpoints = []
        self.mirrors = []
        self.coin_rects = []
        self.off_grid_coin_rects = [] # Rule 1: No Offgrid Coins

        self.player_lives = 3
        self.health_points = 6
        self.spawn_location = (self.tilemap.playerSpawn())  # Default spawn location

        # Pause Initialization
        self.pause = False
        self.changePauseState = True

        # Main Menu Initialization
        self.inMainMenu = True

        self.energy = 100 # Energie, z.B. für Sprinten

        # Dynamically add checkpoints based on map data or predefined positions
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
        for tile in self.tilemap.offgrid_tiles: # RUle 1: No Offgrid Coins
            if tile['type'] == 'coin':
                coin_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], self.tilemap.tile_size, self.tilemap.tile_size)
                self.off_grid_coin_rects.append(coin_rect)
        
        self.inWorld_ItemSelect("middle")

    def inWorld_ItemSelect(self, itemslot):
        self.selected_itemslot = itemslot  # Speichere Auswahl zur Anzeige später
        
    def execute_command(self, command):
        try:
            parts = command.strip().split()
            if not parts:
                return
            
            cmd = parts[0]
            args = parts[1:]
            if cmd == "set_energy" and len(args) == 1:
                value = int(args[0])
                self.energy = value
                self.console_output.append(f"Energy set to {value}")
            elif (cmd == "teleport" or cmd == "teleport") and len(args) == 2:
                x, y = map(int, args)
                self.player.pos = [x, y]
                self.console_output.append(f"Teleported to {x}, {y}")
            elif cmd == "godmode":
                self.health_points = 999
                self.player_lives = 999
                self.console_output.append("Godmode activated")
            elif cmd == "list" and len(args) == 1:
                sub = args[0]
                if sub == 'enemy':
                    for enemy in self.enemies:
                        self.console_output.append(f"Enemy: {enemy.type} at {enemy.pos}")
                elif sub == 'checkpoint':
                    for checkpoint in self.checkpoints:
                        self.console_output.append(f"Checkpoint: {checkpoint}")
                elif sub == 'coin':
                    for coin in self.coin_rects:
                        self.console_output.append(f"Coin: {coin}")
            
            elif cmd == "coin" and len(args) == 2:
                sub = args[0]
                end = args[1]
                if sub == 'give':
                    self.gamesave.updateCoins(self.SAVE_PATH, int(self.gamesave.getCoins(self.SAVE_PATH) + int(end)))
                    self.console_output.append(f"Added {end} coins")
                elif sub == 'remove':
                    self.gamesave.updateCoins(self.SAVE_PATH, int(self.gamesave.getCoins(self.SAVE_PATH) - int(end)))
                    self.console_output.append(f"Removed {end} coins")
                    
            elif cmd == "coin" and len(args) == 1:
                sub = args[0]
                if sub == 'list':
                    self.console_output.append(f"Coins: {self.gamesave.getCoins(self.SAVE_PATH)}")
                
            elif cmd == "help":
                self.console_output.append("Commands: set_energy <val>, teleport <x> <y>, godmode, help")
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


    
    def run(self):
        #Main Game Loop
        while True:
            if self.inMainMenu:
                self.menu.showMainMenu()
                pygame.display.set_caption("MAIN MENU")
                pygame.display.update()
            elif not self.inMainMenu:
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
                            if event.key == pygame.K_LSHIFT and self.energy > 0:  # RUN
                                self.energy -= 0.1
                                self.run_speed = 1.5  # Erhöhe die Geschwindigkeit beim Rennen
                        if event.key == pygame.K_ESCAPE and not self.pause:
                            if self.changePauseState:
                                self.pause = True
                                print(self.pause)
                                self.changePauseState = False
                            elif event.key == pygame.K_ESCAPE and self.pause:
                                if self.changePauseState:
                                    self.pause = False
                                print(self.pause)
                                self.changePauseState = False

                        if event.key == pygame.K_TAB: #s and event.key == pygame.K_t and (event.key == pygame.K_KP_DIVIDE or event.key == pygame.K_SLASH):
                            self.console_active = not self.console_active  # Toggle console

                        elif self.console_active:
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

                    self.display.blit(self.assets['background'], (0, 0))

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



                    self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * self.run_speed, 0))

                    if self.player.collisions['down']:
                        self.jumps_left = 1  # Reset jumps_left when the player lands

                    if self.player.rect().y > self.display.get_height():
                        self.player_lives -= 1
                        if self.player_lives > 0:
                            self.player.pos[0], self.player.pos[1] = self.spawn_location[0], self.spawn_location[1] - 2
                        else:
                            t = pygame.time.get_ticks()
                            print(t/1000)
                            pygame.quit()
                            sys.exit()
                    if self.health_points <= 0:
                        self.player_lives -= 1
                        self.health_points = 6
                        if self.player_lives > 0:
                            self.player.pos[0], self.player.pos[1] = self.spawn_location[0], self.spawn_location[1] - 2
                        else:
                            t = pygame.time.get_ticks()
                            print(t/1000)
                            pygame.quit()
                            sys.exit()

                    life_text = pygame.font.Font.render(pygame.font.Font(None, 24), f"Lives: {self.player_lives}", True, (255, 255, 255))
                    energy_text = pygame.font.Font.render(pygame.font.Font(None, 24), f"Energy: {int(self.energy)}", True, (255, 255, 255))
                    self.display.blit(life_text, (10, 10))
                    self.display.blit(energy_text, (10, 30))
                    if hasattr(self, 'selected_itemslot') and not self.selected_itemslot == "middle":
                        pygame.draw.circle(self.display, (255, 255, 0), (self.display.get_width() // 2, self.display.get_height() // 2), 40, 20)
                    #self.enemyA.attack(self.player.pos, 'fireball', offset=render_scroll)
                    for entity in self.physicsentities:
                        entity.drawHitbox(self.display, offset=render_scroll)


                    self.display.blit(pygame.image.load("assets/images/items/schal_der_leichtigkeit.png"), (100, 100))
                    if self.console_active:
                        pygame.draw.rect(self.display, (0, 0, 0), (0, self.display.get_height() - 60, self.display.get_width(), 60))
                        input_surface = self.consolefont.render(self.console_input, True, (0, 255, 0))
                        self.display.blit(input_surface, (10, self.display.get_height() - 50))

                        for i, line in enumerate(self.console_output[-2:]):  # Show last 2 lines
                            output_surface = self.consolefont.render(line, True, (255, 255, 255))
                            self.display.blit(output_surface, (10, self.display.get_height() - 70 - (20 * i)))

                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                    pygame.display.set_caption('Platformer')
                    pygame.display.update()
                    self.clock.tick(60)
                if self.pause: # PAUSE MENU
                    pygame.display.set_caption('Platformer (Paused)')
                    font = pygame.font.Font(None, 36)
                    text = pygame.font.Font.render(font, "Paused", True, (255, 255, 255))
                    continue_text = pygame.font.Font.render(pygame.font.Font(None, 24), "CONTINUE", True, (255, 255, 255))
                    restart_text = pygame.font.Font.render(pygame.font.Font(None, 24), "RESTART", True, (255, 255, 255))
                    main_menu_text = pygame.font.Font.render(pygame.font.Font(None, 24), "MAIN MENU", True, (255, 255, 255))
                    self.display.blit(text, (self.display.get_width() / 2 - text.get_width() / 2, self.display.get_height() / 2 - self.display.get_height() / 4 - text.get_height() / 2))
                    pygame.draw.rect(self.display, (0, 190, 0), (self.display.get_width() / 2 - text.get_width() / 2 - 10, self.display.get_height() / 2 - self.display.get_height() / 8 - text.get_height() / 2, text.get_width() + 20, text.get_height() - 3))
                    pygame.draw.rect(self.display, (0, 190, 0), (self.display.get_width() / 2 - text.get_width() / 2 - 10, self.display.get_height() / 2 - self.display.get_height() / 4 + text.get_height() + continue_text.get_height() - 1.5, text.get_width() + 20, text.get_height() -3))
                    pygame.draw.rect(self.display, (0, 190, 0), (self.display.get_width() / 2 - text.get_width() / 2 - 10, self.display.get_height() / 2 - self.display.get_height() / 8 - text.get_height() + continue_text.get_height() + restart_text.get_height(), text.get_width() + 20, text.get_height() - 3))
                    self.display.blit(continue_text, (self.display.get_width() / 2 - continue_text.get_width() / 2, self.display.get_height() / 2 - self.display.get_height() / 8 - text.get_height() / 2 + 2))
                    self.display.blit(restart_text, (self.display.get_width() / 2 - restart_text.get_width() / 2, self.display.get_height() / 2 - self.display.get_height() / 4 + text.get_height() + continue_text.get_height()))
                    self.display.blit(main_menu_text, (self.display.get_width() / 2 - main_menu_text.get_width() / 2, self.display.get_height() / 2 - self.display.get_height() / 4 + text.get_height() + continue_text.get_height() + restart_text.get_height()))
                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                    pygame.display.update()
                    self.clock.tick(60)

Game().run()
