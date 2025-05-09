import sys

import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.gamesave import GameSave

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Platformer')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.assets = {
            'grass': load_images('images/tiles/grass'),
            'coin': load_images('images/coin'),
            'player': load_image('images/entities/player.png'),
            'background': load_image('images/background.png'),
            'decor': load_images('images/decor'),
            'checkpoint': load_image('images/checkpoint/checkpoint.png'),
            'mirror': load_image('images/mirror/mirror.png')
        }

        self.worldlist = [
            "1-1", "1-2"
        ]
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('assets/maps/map.json')

        self.gamesave = GameSave()
        self.SAVE_PATH = 'hidden/worlds/save1.json'
        self.gamesave.updateLevel("1-2", {"unlocked": True,"completed": True, "time": 10}, self.SAVE_PATH)
        print(self.gamesave.getCoins(self.SAVE_PATH))


        self.player = Player(self, (self.tilemap.playerSpawn()[0], self.tilemap.playerSpawn()[1]), (8, 15))

        self.scroll = [0, 0]
        
        self.jumps_left = 2  # Initialize jumps_left to allow double jumps

        self.checkpoints = []
        self.mirrors = []
        self.coin_rects = []
        self.player_lives = 3
        self.spawn_location = (self.tilemap.playerSpawn())  # Default spawn location

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
        
    def run(self):
        while True:
            for level in self.worldlist:
                self.gamesave.checkUnlock(level, self.SAVE_PATH)
            self.display.blit(self.assets['background'], (0, 0))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # MOVE LEFT
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT: # MOVE RIGHT
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE: # JUMP
                        if self.jumps_left > 0:
                            self.player.velocity[1] = -3
                            self.jumps_left -= 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            if self.player.collisions['down']:
                self.jumps_left = 2  # Reset jumps_left when the player lands

            if self.player.rect().y > self.display.get_height():
                self.player_lives -= 1
                if self.player_lives > 0:
                    self.player.pos[0], self.player.pos[1] = self.spawn_location[0], self.spawn_location[1] - 2
                else:
                    t = pygame.time.get_ticks()
                    print(t/1000)
                    pygame.quit()
                    sys.exit()
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()