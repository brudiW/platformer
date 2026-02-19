import pygame


def hook():
    player = game.player
    keys = pygame.key.get_pressed()


    if "bogen" not in game.gamesave.items:
        return  # Item nicht eingesammelt → abbrechen
       
    if pygame.joystickCount() > 0: 
    	if game.axrX < 0.5:
            angle = Math.degrees(Math.asin(game.axrX/(Math.sqrt(game.axrX*game.axrX+game.axrY*game.axrY))))
            motion = [0,0]
            motion[1] = Math.sin(Math.radians(angle))*5
            motion[0] = Math.sqrt(5*5-motion[1]*motion[1])
            arrowEntity = PhysicsEntity(game, "arrow", [Math.sqrt(0.7*0.7-(Math.sin(Math.radians(angle))*0.7)*(Math.sin(Math.radians(angle))*0.7))), Math.sin(Math.radians(angle)*0.7)], [0.5, 0.5])
            arrowEntity.velocity = motion
            game.physicsentities.append(arrowEntity)
            while not arrowEntity.collisions["down"]:
                arrowEntity.update()
            game.physicsentities.remove(arrowEntity)
    if pygame.mouse.getPressed(num_buttons=3)[0]:
        mouse_pos = pygame.mouse.getPos()
        rel_pos = [0, 0]
        rel_pos[0] = mouse_pos[0] - game.screen.size[0]/2
        rel_pos[1] = (mouse_pos[1] - game.screen.size[1]/2)*(-1)
        angle = Math.degrees(Math.asin(rel_pos[0]/(Math.sqrt(rel_pos[0]*rel_pos[0]+rel_pos[1]*rel_pos[1]))))
        motion = [0,0]
        motion[1] = Math.sin(Math.radians(angle))*5
        motion[0] = Math.sqrt(5*5-motion[1]*motion[1])
        arrowEntity = PhysicsEntity(game, "arrow", [Math.sqrt(0.7*0.7-(Math.sin(Math.radians(angle))*0.7)*(Math.sin(Math.radians(angle))*0.7)), Math.sin(Math.radians(angle)*0.7)], [0.5, 0.5])
        arrowEntity.velocity = motion
        game.physicsentities.append(arrowEntity)
        while not arrowEntity.collisions["down"]:
            arrowEntity.update()
        game.physicsentities.remove(arrowEntity)


register_hook(hook)
        
            
            
        
