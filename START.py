from scripts.intro import play_intro
import pygame
from game import Game  # oder wie deine Hauptdatei heißt
from scripts.music import MusicPlayer


if __name__ == "__main__":
    pygame.init()
    mp = MusicPlayer()
    mp.play("assets/sounds/intro.mp3", loop=False)  # Musik starten
    play_intro((640, 480))  # Intro anzeigen
    game = Game()  # Spiel danach starten
    game.run()  # Hauptspiel starten