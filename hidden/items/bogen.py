import pygame
import math
import asyncio
from scripts.entities import PhysicsEntity

#async def arrow_update_looper(arrowEntity):
 #   while not arrowEntity.collisions["down"]:
  #      arrowEntity.update(game.tilemap, (0.0))
   # game.physicsentities.remove(arrowEntity)


def hook():
    player = game.player
    keys = pygame.key.get_pressed()


    if "bogen" not in game.gamesave.items:
        return  # Item nicht eingesammelt → abbrechen
       
    if pygame.joystick.get_count() > 0: 
    	if game.axrX < -0.5 or game.axrX > 0.5 or game.axrY < -0.5 or game.axrY > 0.5:
            angle = math.degrees(math.asin(game.axrX/(math.sqrt(game.axrX*game.axrX+game.axrY*game.axrY))))
            motion = [0,0]
            motion[1] = math.sin(math.radians(angle))*5
            motion[0] = math.sqrt(5*5-motion[1]*motion[1])
            arrowEntity = PhysicsEntity(game, "arrow", [math.sqrt(0.7*0.7-(math.sin(math.radians(angle))*0.7)*(math.sin(math.radians(angle))*0.7)), math.sin(math.radians(angle)*0.7)], [0.5, 0.5])
            arrowEntity.velocity = motion
            game.physicsentities.append(arrowEntity)
            #asyncio.run(arrow_update_looper(arrowEntity))
    if pygame.mouse.get_pressed(num_buttons=3)[0]:
        mouse_pos = pygame.mouse.get_pos()
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
        #asyncio.run(arrow_update_looper(arrowEntity))


register_hook(hook)
        
            
            
        
