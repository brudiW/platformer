import pygame
import os
import sys
from scripts.button import Button
pygame.init()



class MainMenu:
  def __init__(self, game):
    self.game = game
    self.menu_state = "main"
    #define fonts
    self.font = pygame.font.SysFont("arialblack", 40)

    #define colours
    self.TEXT_COL = (255, 255, 255)
    
    #load button image
    self.start_img = pygame.image.load("assets/images/button/button_start.png").convert_alpha()
    self.options_img = pygame.image.load("assets/images/button/button_options.png").convert_alpha()
    self.quit_img = pygame.image.load("assets/images/button/button_quit.png").convert_alpha()
    self.video_img = pygame.image.load('assets/images/button/button_video.png').convert_alpha()
    self.audio_img = pygame.image.load('assets/images/button/button_audio.png').convert_alpha()
    self.back_img = pygame.image.load('assets/images/button/button_back.png').convert_alpha()

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
        self.game_menu = False
        self.game.mainstate = "select"
        pygame.time.wait(150)  # Add a 200ms delay
      if self.options_button.draw(self.game.screen):
        self.menu_state = "options"
        pygame.time.wait(150)  # Add a 200ms delay
      if self.quit_button.draw(self.game.screen):
        pygame.quit()
        pygame.time.wait(150)  # Add a 200ms delay
    #check if the options menu is open
    if self.menu_state == "options":
      #draw the different options buttons
      if self.video_button.draw(self.game.screen):
        print("Video Settings")
        pygame.time.wait(150)  # Add a 200ms delay
      if self.audio_button.draw(self.game.screen):
        print("Audio Settings")
        pygame.time.wait(150)  # Add a 200ms delay
      if self.back_button.draw(self.game.screen):
        self.menu_state = "main"
        pygame.time.wait(150)  # Add a 200ms delay

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
