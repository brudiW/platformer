import pygame
import random

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.flip = False
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def getPos(self):
        return self.pos[0], self.pos[1]
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        #print(self.pos)
                
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.game.assets[self.type], self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def renderAtt(self, attack, surf , offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.game.assets[attack], self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    def drawHitbox(self, surf, offset=(0,0)):
        pygame.draw.rect(surf, (255, 0, 0), (self.pos[0] - offset[0], self.pos[1] - offset[1], self.size[0], self.size[1]), 1)

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0


class Enemy(PhysicsEntity):
    def __init__(self, game, e_type, pos, size, attack_type, health):
        super().__init__(game, e_type, pos, size)
        self.attack_type = attack_type
        self.airtime = 0
        self.health = health

    
    def update(self, tilemap, movement=(0, 0)):
        
        super().update(tilemap, self.AI_POS())
        
        self.airtime += 1
        if self.collisions['down']:
            self.airtime = 0
    
    def attack(self, target, attack_type, offset=(0, 0)):
        pygame.draw.line(
            self.game.display,
            (255, 0, 0),
            (self.pos[0]- offset[0], self.pos[1]- offset[1]),
            (target[0] - offset[0], target[1]- offset[1]),
            10
        )
    
    def AI_POS(self):
        # Aktuelle Positionen
        player_x, player_y = self.game.player.getPos()
        enemy_x, enemy_y = self.getPos()
    
        # Abstand berechnen
        dx = player_x - enemy_x
        dy = player_y - enemy_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Bewegung auf Spieler zu
        move_x = 0
        move_y = 0

        if distance < 400:  # Spieler in Sichtweite
            if abs(dx) > 10:
                move_x = 1 if dx > 0 else -1
            if abs(dy) > 50 and self.collisions['down']:  # z. B. springen wenn Spieler über Gegner
                self.velocity[1] = -4  # einfacher Sprung
        else:
            # Patrouillieren oder rumlaufen, wenn Spieler nicht sichtbar
            move_x = random.choice([-1, 0, 1])
            if random.random() < 0.01 and self.collisions['down']:
                self.velocity[1] = -4  # zufälliger Sprung
    
        # Attackieren, wenn nah
        if distance < 120:
            self.attack((player_x, player_y), self.attack_type)

        return move_x, 0
