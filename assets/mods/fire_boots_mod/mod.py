import pygame
class FireBoots(OwnedItem):
    def __init__(self):
        super().__init__(
            name="Fire Boots",
            description="Triples your speed while moving.",
            effect="speed_x3",
            texture=None,
            rarety="epic",
            durability=20,
            game=game
        )
        self.texture = load_asset('fire_boots.png')

    def equip(self, slot):
        if super().equip(slot):
            game.fire_boots_equipped = True
            return True
        return False

    def use(self):
        super().use()

# Register the item
register_item(FireBoots())

# Mod tick hook: apply speed boost on key press
def fire_boots_tick():
    if not getattr(game, 'fire_boots_equipped', False):
        return

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        game.player.velocity[0] = -6  # base speed × 3 (e.g. 2 × 3)
    elif keys[pygame.K_d]:
        game.player.velocity[0] = 6

register_hook(fire_boots_tick)