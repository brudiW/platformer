import os
import pygame

BASE_IMG_PATH = 'assets/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    full_path = BASE_IMG_PATH + path
    if not os.path.exists(full_path):
        print(f"Warning: Directory {full_path} does not exist.")
        return []
    images = []
    for img_name in sorted(os.listdir(full_path)):
        img_path = os.path.join(full_path, img_name)
        images.append(pygame.image.load(img_path).convert_alpha())
    return images