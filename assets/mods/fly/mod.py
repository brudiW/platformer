import pygame

flying_enabled = False

def toggle_fly(*args):
    global flying_enabled
    flying_enabled = not flying_enabled
    if flying_enabled:
        return "Fly mode enabled. Use WASD to move freely."
    else:
        return "Fly mode disabled. Gravity restored."

def hook():
    if flying_enabled:
        # Ignoriere jede Y-Geschwindigkeit durch Gravitation
        game.player.velocity[1] = 0
        
        # Manuelle Steuerung in der Luft
        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_UP]:
            game.player.pos[1] -= speed
        if keys[pygame.K_DOWN]:
            game.player.pos[1] += speed
        if keys[pygame.K_LEFT]:
            game.player.pos[0] -= speed
        if keys[pygame.K_RIGHT]:
            game.player.pos[0] += speed

register_command("fly", toggle_fly)
register_hook(hook)
