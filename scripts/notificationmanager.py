import pygame
import math

class NotificationManager:
    def __init__(self, game):
        self.game = game
        self.notifications = []  # Liste von (Text, Startzeit, Endzeit)
        self.font = pygame.font.SysFont("arialblack", 30)
        self.display_time = 5000  # 5 Sekunden

    def add_notification(self, text):
        current_time = pygame.time.get_ticks()
        end_time = current_time + self.display_time
        self.notifications.append((text, current_time, end_time))

    def update(self):
        current_time = pygame.time.get_ticks()
        self.notifications = [n for n in self.notifications if n[2] > current_time]

    def draw(self):
        if not self.notifications:
            return

        text, start_time, end_time = self.notifications[0]
        now = pygame.time.get_ticks()
        elapsed = now - start_time
        duration = end_time - start_time
        time_left = end_time - now

        # Fading
        if elapsed < 1000:
            alpha = int((elapsed / 1000) * 255)  # Fade-in
        elif time_left < 1000:
            alpha = int((time_left / 1000) * 255)  # Fade-out
        else:
            alpha = 255

        # Wackeln (horizontal sinus)
        wobble = math.sin(now / 100) * 4  # leichte horizontale Bewegung

        # Schweben (vertikal sinus)
        float_y = math.sin(now / 200) * 5  # auf/ab

        # Rendern
        rendered_text = self.font.render(text, True, (255, 255, 255))
        text_surf = pygame.Surface(rendered_text.get_size(), pygame.SRCALPHA)
        text_surf.blit(rendered_text, (0, 0))
        text_surf.set_alpha(alpha)

        # Rechteck vorbereiten
        bg_rect = text_surf.get_rect()
        bg_rect.inflate_ip(20, 10)
        bg_rect.centerx = self.game.screen.get_width() // 2 + wobble
        bg_rect.y = 50 + float_y

        # Hintergrund zeichnen mit Alphakanal
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (0, 0, 0, alpha), bg_surface.get_rect(), border_radius=12)

        # Zeichnen
        self.game.screen.blit(bg_surface, bg_rect)
        self.game.screen.blit(text_surf, (bg_rect.x + 10, bg_rect.y + 5))
