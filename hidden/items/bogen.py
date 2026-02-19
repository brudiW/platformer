import pygame


def hook():
    player = game.player
    keys = pygame.key.get_pressed()


    if "schal_der_leichtigkeit" not in game.gamesave.items:
        return  # Item nicht eingesammelt → abbrechen
       
    if pygame.joystickCount() > 0: 
    	if game.axrX < 0.5:
            angle = Math.degrees(Math.asin(game.axrX/(Math.sqrt(game.axrX*game.axrX+game.axrY*game.axrY))))
            motion = [0,0]
            motion[1] = Math.sin(Math.radians(angle))*5
            motion[0] = Math.sqrt(5*5-motion[1]*motion[1])
            arrowEntity = PhysicsEntity(game, "arrow", player.pos, [0.5, 0.5])
            
        