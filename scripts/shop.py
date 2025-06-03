import pygame

from scripts.utils import load_image



class Shop:
    def __init__(self, game):
        self.game = game
        
    def getShopItems(self):
        print("SHOP:")
        for item in self.game.items.shop_items.values():
            print(f"{item.name}, {item.price}")

    def showShop(self, surf):
        # Berechne Shop-Fenster
        shop_width = surf.get_width() / 3 + surf.get_width() / 4
        shop_height = surf.get_height() / 3 + surf.get_height() / 4
        shop_x = surf.get_width() / 2 - shop_width / 2
        shop_y = surf.get_height() / 2 - shop_height / 2

        # Hintergrund zeichnen
        pygame.draw.rect(surf, (20, 200, 20), (shop_x, shop_y, shop_width, shop_height), width=0, border_radius=20)

        # Fonts vorbereiten
        font = pygame.font.SysFont(None, 20)
        desc_font = pygame.font.SysFont(None, 18)

        # Einstellungen für Items
        item_size = 24
        padding = 10
        text_offset_x = 10
        start_x = shop_x + 20
        start_y = shop_y + 20

        # Mausposition abfragen
        mouse_pos = pygame.mouse.get_pos()

        for index, item in enumerate(self.game.items.shop_items.values()):
            item_y = start_y + index * (item_size + padding)
            item_rect = pygame.Rect(start_x, item_y, item_size, item_size)

            # Rechteck & Bild
            pygame.draw.rect(surf, (255, 255, 255), item_rect, border_radius=5)
            item_img = pygame.transform.scale(load_image(item.texture), (item_size, item_size))
            surf.blit(item_img, item_rect.topleft)

            # Name & Preis daneben
            name_surf = font.render(item.name, True, (0, 0, 0))
            price_surf = font.render(f"{item.price}", True, (0, 0, 0))
            surf.blit(name_surf, (item_rect.right + text_offset_x, item_y))
            surf.blit(price_surf, (item_rect.right + text_offset_x, item_y + 12))

            # Hover: Beschreibung anzeigen
            if item_rect.collidepoint(mouse_pos):
                desc_text = desc_font.render(item.description, True, (255, 255, 255))
                desc_bg = pygame.Surface((desc_text.get_width() + 10, desc_text.get_height() + 6))
                desc_bg.fill((0, 0, 0))
                desc_bg.set_alpha(200)
                desc_pos = (item_rect.right + 100, item_y)  # Versetzt rechts
                surf.blit(desc_bg, desc_pos)
                surf.blit(desc_text, (desc_pos[0] + 5, desc_pos[1] + 3))


