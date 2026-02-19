import pygame
import math
from scripts.entities import PhysicsEntity


def hook():
    player = game.player
    keys = pygame.key.get_pressed()


    if "bogen" not in game.gamesave.items:
        return  # Item nicht eingesammelt → abbrechen
       
    if pygame.joystick.get_count() > 0: 
    	if game.axrX < 0.5:
            angle = math.degrees(math.asin(game.axrX/(math.sqrt(game.axrX*game.axrX+game.axrY*game.axrY))))
            motion = [0,0]
            motion[1] = math.sin(math.radians(angle))*5
            motion[0] = math.sqrt(5*5-motion[1]*motion[1])
            arrowEntity = PhysicsEntity(game, "arrow", [math.sqrt(0.7*0.7-(math.sin(math.radians(angle))*0.7)*(math.sin(math.radians(angle))*0.7)), math.sin(math.radians(angle)*0.7)], [0.5, 0.5])
            arrowEntity.velocity = motion
            game.physicsentities.append(arrowEntity)
            while not arrowEntity.collisions["down"]:
                print("hi")
                #arrowEntity.update()
            game.physicsentities.remove(arrowEntity)
    if pygame.mouse.get_pressed(num_buttons=3)[0]:
        mouse_pos = pygame.mouse.getPos()
        size = game.screen.get_size()
        rel_pos = [0, 0]
        rel_pos[0] = mouse_pos[0] - size[0]/2
        rel_pos[1] = (mouse_pos[1] - size[1]/2)*(-1)
        angle = math.degrees(math.asin(rel_pos[0]/(math.sqrt(rel_pos[0]*rel_pos[0]+rel_pos[1]*rel_pos[1]))))
        motion = [0,0]
        motion[1] = math.sin(math.radians(angle))*5
        motion[0] = math.sqrt(5*5-motion[1]*motion[1])
        arrowEntity = PhysicsEntity(game, "arrow", [math.sqrt(0.7*0.7-(math.sin(math.radians(angle))*0.7)*(math.sin(math.radians(angle))*0.7)), math.sin(math.radians(angle)*0.7)], [0.5, 0.5])
        arrowEntity.velocity = motion
        game.physicsentities.append(arrowEntity)
        while not arrowEntity.collisions["down"]:
            print("hi")
            #arrowEntity.update()
        game.physicsentities.remove(arrowEntity)


register_hook(hook)
        
            
            
        
