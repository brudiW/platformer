import sys
import json
import pygame

from scripts.utils import load_images
#from scripts.tilemap import Tilemap
from scripts.levelselect import Overworld
 
RENDER_SCALE = 2.0

class OverworldEditor:
    def __init__(self):
        #from utils import load_image, load_images
        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.assets = {
            'wgrass': load_images('images/tiles/world 1/grass'),
            'plant': load_images('images/tiles/world 1/plants'),
            'tree': load_images('images/tiles/world 1/tree'),
            'bridge': load_images('images/tiles/world 1/bridge'),
            'cave': load_images('images/tiles/world 1/cave'),
            'castle': load_images('images/tiles/world 1/castle'),
            'path': load_images('images/tiles/world 1/path'),
            'buttons': load_images('images/tiles/world 1/buttons')
        }
        
        self.movement = [False, False, False, False]
        
        self.tilemap = Overworld(self, tile_size=16)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0]
        
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, self.assets, offset=render_scroll)
            
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
            
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)
            
            if self.clicking and self.ongrid:
                if self.tilemap.currentLayer == 0:
                    self.tilemap.layer0[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos, 'layer': self.tilemap.currentLayer}
                if self.tilemap.currentLayer == 1:
                    self.tilemap.layer1[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos, 'layer': self.tilemap.currentLayer}
                if self.tilemap.currentLayer == 2:
                    self.tilemap.layer2[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos, 'layer': self.tilemap.currentLayer}
                if self.tilemap.currentLayer == 3:
                    self.tilemap.layer3[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos, 'layer': self.tilemap.currentLayer}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if self.tilemap.currentLayer == 0:
                    if tile_loc in self.tilemap.layer0:
                        del self.tilemap.layer0[tile_loc]
                if self.tilemap.currentLayer == 1:
                    if tile_loc in self.tilemap.layer1:
                        del self.tilemap.layer1[tile_loc]
                if self.tilemap.currentLayer == 2:
                    if tile_loc in self.tilemap.layer2:
                        del self.tilemap.layer2[tile_loc]
                if self.tilemap.currentLayer == 3:
                    if tile_loc in self.tilemap.layer3:
                        del self.tilemap.layer3[tile_loc]
                
            
            self.display.blit(current_tile_img, (5, 5))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_UP:
                        self.tilemap.currentLayer += 1
                    if event.key == pygame.K_DOWN:
                        self.tilemap.currentLayer -= 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


OverworldEditor().run()
