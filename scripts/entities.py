def AI_POS(self):
    # Aktuelle Positionen
    player_x, player_y = self.game.player.getPos()
    enemy_x, enemy_y = self.getPos()
    
    # Abstand berechnen
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    distance = (dx ** 2 + dy ** 2) ** 0.5

    # Bewegung auf Spieler zu
    move_x = 0
    move_y = 0

    if distance < 400:  # Spieler in Sichtweite
        if abs(dx) > 10:
            move_x = 1 if dx > 0 else -1
        if abs(dy) > 50 and self.collisions['down']:  # z. B. springen wenn Spieler über Gegner
            self.velocity[1] = -4  # einfacher Sprung
    else:
        # Patrouillieren oder rumlaufen, wenn Spieler nicht sichtbar
        move_x = random.choice([-1, 0, 1])
        if random.random() < 0.01 and self.collisions['down']:
            self.velocity[1] = -4  # zufälliger Sprung
    
    # Attackieren, wenn nah
    if distance < 120:
        self.attack((player_x, player_y), self.attack_type)

    return move_x, 0
