import pygame

jump_state = {
    'jump_count': 0,
    'max_jumps': 2,
    'jump_pressed': False,
}

def hook():
    player = game.player
    keys = pygame.key.get_pressed()


    if "schal_der_leichtigkeit" not in game.gamesave.items:
        return  # Item nicht eingesammelt → abbrechen

    # Reset jump on ground
    if player.collisions['down']:
        jump_state['jump_count'] = 0

    # Gamepad-Sprung
    if pygame.joystick.get_count() > 0:
        if game.btnA > 0.5:
            if jump_state['jump_count'] < jump_state['max_jumps']:
                player.velocity[1] = -2.7
                jump_state['jump_count'] += 1

    # Tastatur-Sprung
    if keys[pygame.K_SPACE]:
        if not jump_state['jump_pressed']:
            if jump_state['jump_count'] < jump_state['max_jumps']:
                player.velocity[1] = -2.7
                jump_state['jump_count'] += 1
        jump_state['jump_pressed'] = True
    else:
        jump_state['jump_pressed'] = False

register_hook(hook)
