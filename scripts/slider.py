import pygame

class Slider:
    def __init__(self, x, y, w, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, w, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.handle_rect = pygame.Rect(x + (start_val - min_val) / (max_val - min_val) * w - 5, y - 5, 10, 20)
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, (180, 180, 180), self.rect)  # slider background
        pygame.draw.rect(surface, (100, 100, 255), self.handle_rect)  # handle

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = min(max(event.pos[0], self.rect.x), self.rect.x + self.rect.width)
            self.handle_rect.x = new_x - self.handle_rect.width // 2
            self.value = self.min_val + ((self.handle_rect.x - self.rect.x) / self.rect.width) * (self.max_val - self.min_val)

    def get_value(self):
        return self.value
