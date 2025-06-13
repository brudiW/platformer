import sys
import subprocess
import pkg_resources

# -------------------------
# Prüfen & ggf. installieren von pygame
# -------------------------
def ensure_pygame():
    try:
        import pygame  # noqa
    except ImportError:
        print("📦 pygame wird installiert...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

# Führe das vor allem anderen aus
ensure_pygame()

# -------------------------
# Hauptspiel starten
# -------------------------
import pygame
from scripts.intro import play_intro
from game import Game
from scripts.music import MusicPlayer

if __name__ == "__main__":
    pygame.init()
    mp = MusicPlayer()
    mp.play("assets/sounds/intro.mp3", loop=False)  # Musik starten
    play_intro((640, 480))  # Intro anzeigen
    game = Game()  # Spiel danach starten
    game.run()  # Hauptspiel starten
