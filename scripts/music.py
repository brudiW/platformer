import sys, os, pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.sfx_volume = 0.5
        self.music_volume = 0.5
        pygame.mixer.music.set_volume(self.music_volume)

    def play(self, path: str, loop=False):
        """
        Spielt Musik ab (nur eine gleichzeitig möglich).
        
        Args:
            path (str): Pfad zur Musikdatei.
            loop (bool): Ob die Musik in einer Schleife abgespielt werden soll.
        """
        if not os.path.exists(path):
            print(f"Music file {path} does not exist.")
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        """Stoppt die aktuell abgespielte Musik."""
        pygame.mixer.music.stop()

    def play_sound(self, path: str):
        """
        Spielt einen Soundeffekt ab (mehrere gleichzeitig möglich).
        
        Args:
            path (str): Pfad zur Sounddatei.
        """
        if not os.path.exists(path):
            print(f"Sound file {path} does not exist.")
            return
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.sfx_volume)
        sound.play()

    def set_music_volume(self, volume: float):
        """
        Setzt die Lautstärke der Musik.

        Args:
            volume (float): Lautstärke zwischen 0.0 und 1.0.
        """
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_sfx_volume(self, volume: float):
        """
        Setzt die Lautstärke der Soundeffekte.
        Args:
            volume (float): Lautstärke zwischen 0.0 und 1.0.
        """
        self.sfx_volume = volume
