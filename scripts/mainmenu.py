import pygame
import os
import sys
import datetime
from scripts.button import Button
from scripts.slider import Slider
pygame.init()



class MainMenu:
	def __init__(self, game):
		pygame.init()
		self.game = game
		self.menu_state = "main"
		#define fonts
		self.font = pygame.font.SysFont("arialblack", 40)
		#self.screen = pygame.display.set_mode((640, 480))
		#self.display = pygame.Surface((320, 240))
		# Audio sliders
		self.music_slider = Slider(250, 150, 300, 0.0, 1.0, 0.5)
		self.sfx_slider = Slider(250, 250, 300, 0.0, 1.0, 0.5)


    	#define colours
		self.TEXT_COL = (255, 255, 255)
    
   	 	#load button image
		self.start_img = pygame.image.load("assets/images/button/button_start.png").convert()
		self.options_img = pygame.image.load("assets/images/button/button_options.png").convert()
		self.quit_img = pygame.image.load("assets/images/button/button_quit.png").convert()
		self.video_img = pygame.image.load('assets/images/button/button_video.png').convert()
		self.audio_img = pygame.image.load('assets/images/button/button_audio.png').convert()
		self.back_img = pygame.image.load('assets/images/button/button_back.png').convert()

    	#create button instances
		self.start_button = Button(304, 125, self.start_img, 1)
		self.options_button = Button(297, 250, self.options_img, 1)
		self.quit_button = Button(336, 375, self.quit_img, 1)
		self.video_button = Button(226, 125, self.video_img, 1)
		self.audio_button = Button(225, 250, self.audio_img, 1)
		self.back_button = Button(332, 375, self.back_img, 1)
	def draw_text(self, text, font, text_col, x, y):
		self.img = font.render(text, True, text_col)
		self.game.screen.blit(self.img, (x, y))
	def showMainMenu(self):
			self.game.screen.fill((52, 78, 91))
    	#check menu state
			if self.menu_state == "main":
      			#draw pause screen buttons
				if self.start_button.draw(self.game.screen):
					#self.game_menu = False
					self.game.mainstate = "select"
					self.game.mp.play("assets/sounds/Overworld.mp3", loop=True)
					pygame.time.wait(150)  # Add a 200ms delay
				if self.options_button.draw(self.game.screen):
					self.menu_state = "options"
					pygame.time.wait(150)  # Add a 200ms delay
				if self.quit_button.draw(self.game.screen):
					pygame.quit()
					sys.exit()
    		#check if the options menu is open
			if self.menu_state == "options":
      			#draw the different options buttons
				if self.video_button.draw(self.game.screen):
					print("Video Settings")
					pygame.time.wait(150)  # Add a 200ms delay
				if self.audio_button.draw(self.game.screen):
					self.menu_state = "audio"
					pygame.time.wait(150)  # Add a 200ms delay
				if self.back_button.draw(self.game.screen):
					self.menu_state = "main"
					pygame.time.wait(150)  # Add a 200ms delay
			if self.menu_state == "audio":
				self.draw_text("Musiklautstärke", self.font, self.TEXT_COL, 50, 140)
				self.draw_text("Effektlautstärke", self.font, self.TEXT_COL, 50, 240)
				self.music_slider.draw(self.game.screen)
				self.sfx_slider.draw(self.game.screen)
				# Lautstärke setzen (optional direkt, sonst extern auslesen)
				pygame.mixer.music.set_volume(self.music_slider.get_value())
				# Soundeffekte -> später beim Abspielen jeweils set_volume(self.sfx_slider.get_value())
				if self.back_button.draw(self.game.screen):
					self.menu_state = "options"
					pygame.time.wait(150)


    		#event handler
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if self.menu_state == "audio":
					self.music_slider.handle_event(event)
					self.sfx_slider.handle_event(event)