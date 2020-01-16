from os import path
import pygame
from image import load_image

NUMBER_NIK = 2
LENGTH_LASER = 50
WIDTH_LASER = 50
INIT_ENERGY = 100
LENGTH_DROID = 50
WIDTH_DROID = 50
LENGTH_SPACESHIP = 40
WIDTH_SPACESHIP = 80
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800
DISPLAYMODE = (WINDOW_WIDTH, WINDOW_HEIGHT)
TEXTCOLOR = (255, 255, 255)
FPS = 40
MAX_NUMBER_DROIDS = 3
ASTEROID_MIN_SPEED = 1
ASTEROID_SIZE = 55
ASTEROID_MAX_SPEED = 8
DELAY_EXPLOSION = 5  # Для амитации задержки анимации взрыва
ADDNEW_ASTEROID_RATE = 7
RATE_PLAYER_SPEED = 6
PROB_ENERGETIC_ASTEROID = 0.4  # Вероятность, которая определяет, является ли это энергичным астероидом.

# Шрифты
pygame.init()
window = pygame.display.set_mode(DISPLAYMODE)
font_1 = pygame.font.SysFont("RetroComputer[RUS by Daymarius]", 22)
font_2 = pygame.font.SysFont("RetroComputer[RUS by Daymarius]", 100)


# Фоновое изображение
background = load_image(path.join('data', 'images', 'background', 'background_1.jpg'), True, DISPLAYMODE)

window.blit(background, (0, 0))
