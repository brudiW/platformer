import pygame
import button

pygame.init()

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_menu = True
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
start_img = pygame.image.load("images/button/button_start.png").convert_alpha()
options_img = pygame.image.load("images/button/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button/button_audio.png').convert_alpha()
back_img = pygame.image.load('images/button/button_back.png').convert_alpha()

#create button instances
start_button = button.Button(304, 125, start_img, 1)
options_button = button.Button(297, 250, options_img, 1)
quit_button = button.Button(336, 375, quit_img, 1)
video_button = button.Button(226, 125, video_img, 1)
audio_button = button.Button(225, 250, audio_img, 1)
back_button = button.Button(332, 375, back_img, 1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
run = True
while run:

  screen.fill((52, 78, 91))

  #check if game is paused
  if game_menu:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if start_button.draw(screen):
        game_menu = False
        pygame.time.wait(150)  # Add a 200ms delay
      if options_button.draw(screen):
        menu_state = "options"
        pygame.time.wait(150)  # Add a 200ms delay
      if quit_button.draw(screen):
        run = False
        pygame.time.wait(150)  # Add a 200ms delay
    #check if the options menu is open
    if menu_state == "options":
      #draw the different options buttons
      if video_button.draw(screen):
        print("Video Settings")
        pygame.time.wait(150)  # Add a 200ms delay
      if audio_button.draw(screen):
        print("Audio Settings")
        pygame.time.wait(150)  # Add a 200ms delay
      if back_button.draw(screen):
        menu_state = "main"
        pygame.time.wait(150)  # Add a 200ms delay

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      run = False
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()