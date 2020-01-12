from os import path
import pygame


def load_image(path, use_transparency=False, rect_img=(0, 0)):
    width, height = rect_img
    try:  # Загрузка изображения
        image = pygame.image.load(path)
    except pygame.error:
        print("Could not load the image: ", path)
        raise SystemExit
    if use_transparency:
        image = image.convert()
    else:  # Проверяем и добавляем прозрачность
        image = image.convert_alpha()
    if width >= 1 and height >= 1:  # Масштабировать изображение до указанного размера
        image = scale_image(image, (width, height))
    return image


def scale_image(image, size_required):
    scaled_img = pygame.transform.scale(image, size_required)
    return scaled_img

INIT_ENERGY = 100
LENGTH_SPACESHIP = 50
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750
DISPLAYMODE = (WINDOW_WIDTH, WINDOW_HEIGHT)
TEXTCOLOR = (255, 255, 255)
FPS = 40
MAX_NUMBER_DROIDS = 3
ASTEROID_MIN_SPEED = 1
ASTEROID_SIZE = 70
ASTEROID_MAX_SPEED = 8
DELAY_EXPLOSION = 5  # Для амитации задержки анимации взрыва
ADDNEW_ASTEROID_RATE = 7
RATE_PLAYER_SPEED = 6
PROB_ENERGETIC_ASTEROID = 0.4  # Вероятность, которая определяет, является ли это энергичным астероидом.

# Шрифты
pygame.init()
window = pygame.display.set_mode(DISPLAYMODE)
font_1 = pygame.font.SysFont("DS Sofachrome", 12)
font_2 = pygame.font.SysFont("Liberation Serif", 20)
font_3 = pygame.font.SysFont("Arial", 20)
font_4 = pygame.font.SysFont("Times New Roman", 36)
font_5 = pygame.font.SysFont("Liberation Serif", 40)  # Points

# Фоновое изображение
background = load_image(path.join('data', 'images', 'background', 'background.jpg'), True, DISPLAYMODE)

window.blit(background, (0, 0))