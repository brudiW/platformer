import sys

import pygame

import json

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.gamesave import GameSave
from scripts.item import Item, ShopItem, CollectableItem, OwnedItem, Items

class Game:
    def __init__(self):
        pygame.init()
        if pygame.joystick.get_count() > 0:
            self.joy = pygame.joystick.Joystick(0)

        pygame.display.set_caption('Platformer')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.items = Items(self)

        self.items.loadItems('hidden/items.json')
        
        
        
        self.movement = [False, False]
        
        self.assets = {
            'grass': load_images('images/tiles/grass'),
            'coin': load_images('images/coin'),
            'player': load_image('images/checkpoint/checkpoint.png'),
            'background': load_image('images/background.png'),
            'decor': load_images('images/decor'),
            'checkpoint': load_image('images/checkpoint/checkpoint.png'),
            'mirror': load_image('images/mirror/mirror.png'),
            'stone': load_images('images/tiles/stone'),
        }

        self.worldlist = [
            "1-1", "1-2"
        ]
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('assets/maps/1-1.json')

        self.gamesave = GameSave()
        self.SAVE_PATH = 'hidden/worlds/save1.json'
        self.gamesave.updateLevel("1-2", {"unlocked": True,"completed": True, "time": 10}, self.SAVE_PATH)
        print(self.gamesave.getCoins(self.SAVE_PATH))


        self.player = Player(self, (self.tilemap.playerSpawn()[0], self.tilemap.playerSpawn()[1]), (8, 15))

        self.scroll = [0, 0]
        
        self.jumps_left = 1  # Initialize jumps_left to allow double jumps
        self.run_speed = 0.5  # Zusätzliche Geschwindigkeit beim Rennen

        self.checkpoints = []
        self.mirrors = []
        self.coin_rects = []
        self.off_grid_coin_rects = []
        self.player_lives = 3
        self.spawn_location = (self.tilemap.playerSpawn())  # Default spawn location
        self.pause = False
        self.changePauseState = True

        self.energy = 100

        # Dynamically add checkpoints based on map data or predefined positions
        for tile in self.tilemap.tilemap.values():
            if tile['type'] == 'checkpoint':
                checkpoint_rect = pygame.Rect(tile['pos'][0] * self.tilemap.tile_size, tile['pos'][1] * self.tilemap.tile_size, self.tilemap.tile_size, self.tilemap.tile_size)
                self.checkpoints.append(checkpoint_rect)
            if tile['type'] == 'mirror':
                mirror_rect = pygame.Rect(tile['pos'][0] * self.tilemap.tile_size, tile['pos'][1] * self.tilemap.tile_size, self.tilemap.tile_size, self.tilemap.tile_size)
                self.mirrors.append(mirror_rect)
            if tile['type'] == 'coin':
                coin_rect = pygame.Rect(tile['pos'][0] * self.tilemap.tile_size, tile['pos'][1] * self.tilemap.tile_size, self.tilemap.tile_size, self.tilemap.tile_size)
                self.coin_rects.append(coin_rect)
        for tile in self.tilemap.offgrid_tiles:
            if tile['type'] == 'coin':
                coin_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], self.tilemap.tile_size, self.tilemap.tile_size)
                self.off_grid_coin_rects.append(coin_rect)
        
    def run(self):
        while True:
            if pygame.joystick.get_count() > 0:
                self.axlX = self.joy.get_axis(0) # laufen l = -1, r = 1
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
                for level in self.worldlist:
                    self.gamesave.checkUnlock(level, self.SAVE_PATH)
                self.display.blit(self.assets['background'], (0, 0))
            
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
                self.tilemap.render(self.display, offset=render_scroll)
            
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
            
            
                        
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

                life_text = pygame.font.Font.render(pygame.font.Font(None, 24), f"Lives: {self.player_lives}", True, (255, 255, 255))
                energy_text = pygame.font.Font.render(pygame.font.Font(None, 24), f"Energy: {int(self.energy)}", True, (255, 255, 255))
                self.display.blit(life_text, (10, 10))
                self.display.blit(energy_text, (10, 30))
            
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                pygame.display.set_caption('Platformer')
                pygame.display.update()
                self.clock.tick(60)
            if self.pause:
                pygame.display.set_caption('Platformer (Paused)')
                font = pygame.font.Font(None, 36)
                text = pygame.font.Font.render(font, "Paused", True, (255, 255, 255))
                continue_text = pygame.font.Font.render(font, "CONTINUE", True, (255, 255, 255))
                restart_text = pygame.font.Font.render(font, "RESTART", True, (255, 255, 255))
                main_menu_text = pygame.font.Font.render(font, "MAIN MENU", True, (255, 255, 255))
                self.display.blit(text, (self.display.get_width() / 2 - text.get_width() / 2, self.display.get_height() / 2 - self.display.get_height() / 4 - text.get_height() / 2))
                pygame.draw.rect(self.display, (0, 190, 0), (self.display.get_width() / 2 - text.get_width() / 2 - 10, self.display.get_height() / 2 - self.display.get_height() / 8 - text.get_height() / 2, text.get_width() + 20, text.get_height() + 20))
                self.display.blit(continue_text, (self.display.get_width() / 2 - continue_text.get_width() / 2, self.display.get_height() / 2 - self.display.get_height() / 4 + text.get_height() / 2))
                self.display.blit(restart_text, (self.display.get_width() / 2 - restart_text.get_width() / 2, self.display.get_height() / 2 - self.display.get_height() / 4 + text.get_height() + continue_text.get_height()))
                self.display.blit(main_menu_text, (self.display.get_width() / 2 - main_menu_text.get_width() / 2, self.display.get_height() / 2 - self.display.get_height() / 4 + text.get_height() + continue_text.get_height() + restart_text.get_height()))
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                pygame.display.update()
                self.clock.tick(60)

Game().run()
