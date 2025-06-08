# intro.py
import pygame
import random
import sys

def play_intro(screen_size=(800, 600)):
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    logo = pygame.image.load("assets/images/logo/logo.png").convert_alpha()
    logo = pygame.transform.smoothscale(logo, (400, 400))
    font = pygame.font.SysFont("consolas", 32)
    start_text = font.render("Press Start", True, (0, 255, 0))

    fog_particles = []
    for _ in range(50):
        fog_particles.append({
            'x': random.randint(0, screen_size[0]),
            'y': random.randint(screen_size[1] - 100, screen_size[1]),
            'alpha': random.randint(50, 120),
            'radius': random.randint(20, 50)
        })

    def draw_fog():
        for p in fog_particles:
            surface = pygame.Surface((p['radius'] * 2, p['radius'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (0, 255, 0, p['alpha']), (p['radius'], p['radius']), p['radius'])
            screen.blit(surface, (p['x'], p['y']))
            p['x'] += random.randint(-1, 1)
            p['y'] += random.choice([-0.2, -0.1, 0])
            if p['y'] < screen_size[1] - 200:
                p['y'] = screen_size[1] - 50

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 9000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        draw_fog()

        elapsed = pygame.time.get_ticks() - start_time
        alpha = min(255, int((elapsed / 3000) * 255))
        logo_copy = logo.copy()
        logo_copy.set_alpha(alpha)
        screen.blit(logo_copy, (screen_size[0] // 2 - 200, screen_size[1] // 2 - 200))

        if 6000 < elapsed < 9000:
            if (elapsed // 500) % 2 == 0:
                screen.blit(start_text, (screen_size[0] // 2 - start_text.get_width() // 2, screen_size[1] - 100))

        pygame.display.flip()
        clock.tick(60)

    pygame.display.quit()  # Wichtiger Schritt!
