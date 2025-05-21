import pygame

jump_state = {
    'jump_count': 0,
    'max_jumps': 2,
    'jump_pressed': False,
}

def hook():
    keys = pygame.key.get_pressed()
    player = game.player

    # Reset jump on ground
    if player.collisions['down']:
        jump_state['jump_count'] = 0
        
    if pygame.joystick.get_count() > 0:
        if game.btnA > 0.5: # JUMP
            if jump_state['jump_count'] < jump_state['max_jumps']:
                player.velocity[1] = -2.7
                jump_state['jump_count'] += 1

    if keys[pygame.K_SPACE]:
        if not jump_state['jump_pressed']:
            if jump_state['jump_count'] < jump_state['max_jumps']:
                player.velocity[1] = -2.7
                jump_state['jump_count'] += 1
        jump_state['jump_pressed'] = True
    else:
        jump_state['jump_pressed'] = False

    

register_hook(hook)
