import json

import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass','stone'}
AUTOTILE_TYPES = {'grass','stone','coin'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.header = {}
        self.tilemap = {}
        self.offgrid_tiles = {}    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'header': self.header, 'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
        
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.header = map_data['header']
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
        print(self.header)
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def playerSpawn(self):
        self.spawn = self.header['worldSpawn']
        return self.spawn[0], self.spawn[1]
        
    def getBackground(self):
        self.backgrund = self.header['background']
        return self.backgrund


    def render(self, surf, offset=(0, 0)):
        for coin in self.game.coin_rects:  # Copy for safe removal
            if self.game.player.rect().colliderect(coin):
                self.game.coin_rects.remove(coin)
                self.tilemap.pop(f"{int(coin.x/self.tile_size)};{int(coin.y/self.tile_size)}")
            else:
                surf.blit(self.game.assets['coin'][0], (coin.x - offset[0], coin.y - offset[1]))
                
        #print("Coin Length: ", len(self.game.coin_rects))

            
        for tile in self.offgrid_tiles:
            if tile['type'] in self.game.assets:
                asset = self.game.assets[tile['type']]
                if isinstance(asset, list):
                    if 0 <= tile['variant'] < len(asset):
                        surf.blit(asset[tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                    else:
                        # Use the first variant as a fallback if the index is out of range
                        surf.blit(asset[0], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                else:
                    surf.blit(asset, (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    if tile['type'] in self.game.assets:
                        asset = self.game.assets[tile['type']]
                        if isinstance(asset, list):
                            if 0 <= tile['variant'] < len(asset):
                                surf.blit(asset[tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                            else:
                                # Use the first variant as a fallback if the index is out of range
                                surf.blit(asset[0], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                        else:
                            surf.blit(asset, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        
        

        for checkpoint in self.game.checkpoints:
            if self.game.player.rect().colliderect(checkpoint):
                self.game.spawn_location = (checkpoint.x, checkpoint.y)
                self.game.checkpoints.remove(checkpoint)  # Optional: Remove checkpoint after activation
            else:
                surf.blit(self.game.assets['checkpoint'], (checkpoint.x - offset[0], checkpoint.y - offset[1]))
        
        for mirror in self.game.mirrors[:]:
            if self.game.player.rect().colliderect(mirror):
                pygame.quit()
            else:
                surf.blit(self.game.assets['mirror'], (mirror.x - offset[0], mirror.y - offset[1]))
