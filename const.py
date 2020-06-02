# coding=utf-8

# //////////////////
# ФАЙЛ КОНСТАНТ
# //////////////////

import pygame
import os


# Функция подключения файлов со звуком
def load_sound(filename, sound_lvl=1.0):
    path = os.path.join('static', 'sound', filename)  # Получаем путь к файлу
    sound = pygame.mixer.Sound(path)  # Загрузка мелодий
    sound.set_volume(sound_lvl)  # Настройка громкости звука
    return sound


# инициализация Pygame:
pygame.init()

# Размеры изображения игорка
LENGTH_SPACESHIP = 32
WIDTH_SPACESHIP = 64

# Размеры изображения врага
LENGTH_DROID = 50
WIDTH_DROID = 50

# Размеры изображения лазеров
LENGTH_LASER = 50
WIDTH_LASER = 50

# Размеры изображения астероида
LENGTH_ASTEROID = 55
WIDTH_ASTEROID = 55

# Размеры изображения энергии
LENGTH_ENERGY = 20
WIDTH_ENERGY = 20

# Размеры экрана игры
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800
DISPLAYMODE = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(DISPLAYMODE)  # Устанавливаю размер экрана

# Количество энергии игрока
INIT_ENERGY = 100
COUNT_LASER_BAR = 50  # Максимальное количество лазера у игрока

# Количество fps
FPS = 40

RATE_PLAYER_SPEED = 6  # Устанавливаю скорость игрока
ASTEROID_MIN_SPEED = 1  # Устанавливаю минимальную скорость астероида
ASTEROID_MAX_SPEED = 8  # Устанавливаю максимальную скорость астероида

NUMBER_NIK = 2  # Количество ников

MAX_NUMBER_DROIDS = 3  # Устанавливаю максимальное количество врагов на экране (в один момент времени)

DELAY = 5   # Устанавливаю задержку смены изображений
ADD_NEW_ASTEROID_RATE = 7  # Количество идераций цикла после которых создается новый астероид

PROB_ENERGETIC_ASTEROID = 0.4  # Вероятность, которая определяет, является ли это энергичным астероидом.

# Устанавливаю количество кадров у спрайтов
COUNT_PLAYER = 10
COUNT_DROID = 2
COUNT_EXPLOSION = 6
COUNT_LASER = 4

# =======
# ШРИФТЫ
# =======

TEXT_COLOR = (255, 255, 255)  # Цвет шрифта белый
font_1 = pygame.font.SysFont("RetroComputer[RUS by Daymarius]", 22)  # Устанавливаю название и размер шрифта №1
font_2 = pygame.font.SysFont("RetroComputer[RUS by Daymarius]", 100)  # Устанавливаю название и размер шрифта №2

# =======
# ЗВУКИ
# =======

intro_sound = load_sound('intro.ogg', 0.3)  # Звук заставки
explosion_sound = load_sound('explosion_explosion.ogg', 0.3)  # Звук взрыва
energy_sound = load_sound('energy.ogg', 0.3)  # Звук пойманой энергии
game_over_sound = load_sound('game_over.ogg', 1.0)  # Звук проигрыша
game_won_sound = load_sound('game_won.ogg', 1.0)  # Звук победы
laser_droid_sound = load_sound("laser_droid.ogg", 0.3)  # Звук выстрела лазера врага
laser_player_sound = load_sound('laser_player.ogg', 0.3)  # Звук  выстрела лазера игрока
explosion_player = load_sound("explosion_player.ogg", 0.3)  # Звук взрыва игрока
explosion_droid = load_sound("explosion_droid.ogg", 0.3)  # Звук взрыва врага
explosion_asteroid = load_sound("destroyed_asteroid.ogg", 0.3)  # Звук взрыва астероида

music_channel = pygame.mixer.Channel(4)
