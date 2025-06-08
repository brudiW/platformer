import os
import sys
import pygame
import json
import math
from scripts.utils import load_image, load_images

#from scripts.button import Button


RENDER_SCALE = 2.0
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

class LevelSelect:
    def __init__(self, game, display):
        from scripts.utils import load_image, load_images
        pygame.init()
        self.overworld = Overworld(game, 16)
        self.overworld.load('map.json')
        self.game = game
        self.display = display
        self.pos = [0, 0]
        self.direction = [0, 0]
        self.figur = pygame.Rect(self.pos[0], self.pos[1], 5, 13)
        self.scroll = [0, 0]
        self.buttons = []

        self.clock = pygame.time.Clock()

        self.assets = {
            'player': load_image('assets/images/entities/player.png'),
            'wgrass': load_images('assets/images/tiles/world 1/grass'),
            'plant': load_images('assets/images/tiles/world 1/plants'),
            'tree': load_images('assets/images/tiles/world 1/tree'),
            'bridge': load_images('assets/images/tiles/world 1/bridge'),
            'cave': load_images('assets/images/tiles/world 1/cave'),
            'castle': load_images('assets/images/tiles/world 1/castle'),
            'path': load_images('assets/images/tiles/world 1/path'),
            'buttons': load_images('assets/images/tiles/world 1/buttons')
        }
        self.flip = False
        self.buttonAs = []
        self.buttonBs = []


        for tile in self.overworld.layer0.values():
            self.overworld.layers[tile['pos'][0], tile['pos'][1]] = tile
        for tile in self.overworld.layer1.values():
            self.overworld.layers[tile['pos'][0], tile['pos'][1]] = tile
        for tile in self.overworld.layer2.values():
            self.overworld.layers[tile['pos'][0], tile['pos'][1]] = tile
        for tile in self.overworld.layer3.values():
            self.overworld.layers[tile['pos'][0], tile['pos'][1]] = tile

        for tile in self.overworld.layers.values():
            if tile['type'] == 'buttons':
                button_rect = pygame.Rect(tile['pos'][0] * self.overworld.tile_size, tile['pos'][1] * self.overworld.tile_size, self.overworld.tile_size, self.overworld.tile_size)
                self.buttons.append(button_rect)


    def getPos(self):
        return self.pos[0], self.pos[1]

    def move(self, direction, offset=(0, 0)):
        #for tile in self.overworld.getCollisionRects(self.pos):
            #if not self.figur.colliderect(tile):
        if not direction[0] == 0:
            self.pos[0] += direction[0]
        if not direction[1] == 0:
            self.pos[1] += direction[1]
        if self.pos[0] < -100:
            self.game.mainstate = "start"
            self.reset()
    
    def render(self, offset=(0, 0)):
        self.figur = pygame.Rect(self.pos[0], self.pos[1], 5, 13)
        #pygame.draw.rect(self.display, (255, 0, 0), (self.pos[0] - offset[0], self.pos[1] - offset[1], 5, 13), 1)

    def reset(self):
        self.pos = [0, 0]
        self.direction = [0, 0]
        self.figur = pygame.Rect(self.pos[0], self.pos[1], 5, 13)
        self.scroll = [0, 0]


    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction[0] = -1
                elif event.key == pygame.K_RIGHT:
                    self.direction[0] = 1
                if event.key == pygame.K_UP:
                    self.direction[1] = -1
                elif event.key == pygame.K_DOWN:
                    self.direction[1] = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.direction[0] = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.direction[1] = 0


        self.move(self.direction)
        self.display.fill((0, 0, 0))
            
        self.scroll[0] += (self.figur.centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.figur.centery - self.display.get_height() / 2 - self.scroll[1]) / 30
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        
        self.overworld.render(self.display, self.assets, offset=render_scroll)
        if self.direction[0] > 0:
            self.flip = False
        if self.direction[0] < 0:
            self.flip = True
        self.display.blit(pygame.transform.flip(self.assets['player'], self.flip, False), (self.pos[0] - render_scroll[0], self.pos[1] - render_scroll[1]))
        self.render(offset=render_scroll)


class Overworld:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.currentLayer = 1
        self.layer0 = {}
        self.layer1 = {}
        self.layer2 = {}
        self.layer3 = {}
        self.layers = {}


    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'layer0': self.layer0, 'layer1': self.layer1, 'layer2': self.layer2, 'layer3': self.layer3, 'tile_size': self.tile_size}, f)
        f.close()
        
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.layer0 = map_data['layer0']
        self.layer1 = map_data['layer1']
        self.layer2 = map_data['layer2']
        self.layer3 = map_data['layer3']

    def getCollisionRects(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def matchButton(self, button):
        x = math.floor(int(button.x / self.tile_size))
        y = math.floor(int(button.y / self.tile_size))
        match (x,y):
            case (9, 0):
                self.game.loadWorld("assets/maps/1-1.json")
                self.game.ls.reset()
                self.game.mainstate = 'game'
                self.game.mp.play('assets/sounds/1-1_and_1-3.mp3', loop=True)
            case (18, -6): 
                self.game.loadWorld("assets/maps/1-2.json")
                self.game.ls.reset()
                self.game.mainstate = 'game'
                self.game.mp.play('assets/sounds/1-2.mp3', loop=True)
            case (27, 0):
                self.game.loadWorld("assets/maps/1-3.json")
                self.game.ls.reset()
                self.game.mainstate = 'game'
                self.game.mp.play('assets/sounds/1-1_and_1-3.mp3', loop=True)
            # case (33, 7):
            #     self.game.loadWorld("assets/maps/1-3.json")
            #     self.game.ls.reset()
            #     self.game.mainstate = 'game'
            
            # case (43, 0):
            #     self.game.loadWorld("assets/maps/1-5.json")
            #     self.game.ls.reset()
            #     self.game.mainstate = 'game'

    def render(self, display, assets, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + display.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + display.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.layer0:
                    tile = self.layer0[loc]
                    if tile['type'] in assets:
                        asset = assets[tile['type']]
                        if isinstance(asset, list):
                            if 0 <= tile['variant'] < len(asset):
                                display.blit(asset[tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                            else:
                                # Use the first variant as a fallback if the index is out of range
                                display.blit(asset[0], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                        else:
                            display.blit(asset, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                if loc in self.layer1:
                    tile = self.layer1[loc]
                    if tile['type'] in assets:
                        asset = assets[tile['type']]
                        if isinstance(asset, list):
                            if 0 <= tile['variant'] < len(asset):
                                display.blit(asset[tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                            else:
                                # Use the first variant as a fallback if the index is out of range
                                display.blit(asset[0], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                        else:
                            display.blit(asset, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                if loc in self.layer2:
                    tile = self.layer2[loc]
                    if tile['type'] in assets:
                        asset = assets[tile['type']]
                        if isinstance(asset, list):
                            if 0 <= tile['variant'] < len(asset):
                                display.blit(asset[tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                            else:
                                # Use the first variant as a fallback if the index is out of range
                                display.blit(asset[0], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                        else:
                            display.blit(asset, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                if loc in self.layer3:
                    tile = self.layer3[loc]
                    if tile['type'] in assets:
                        asset = assets[tile['type']]
                        if isinstance(asset, list):
                            if 0 <= tile['variant'] < len(asset):
                                display.blit(asset[tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                            else:
                                # Use the first variant as a fallback if the index is out of range
                                display.blit(asset[0], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                        else:
                            display.blit(asset, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        for button in self.game.ls.buttons:
            if self.game.ls.figur.colliderect(button):
                display.blit(self.game.ls.assets['buttons'][1], (button.x - offset[0], button.y - offset[1]))
                self.matchButton(button)
                