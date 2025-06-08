import sys, os, pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.sfx_volume = 0.5
        self.music_volume = 0.5
        pygame.mixer.music.set_volume(self.music_volume)

    def play(self, path, loop=False):
        """Spielt Musik ab (nur eine gleichzeitig möglich)."""
        if not os.path.exists(path):
            print(f"Music file {path} does not exist.")
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sound(self, path):
        """Spielt einen Soundeffekt ab (mehrere gleichzeitig möglich)."""
        if not os.path.exists(path):
            print(f"Sound file {path} does not exist.")
            return
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.sfx_volume)
        sound.play()

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
