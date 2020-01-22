# coding=utf-8
import pygame
import os
# Файл констант


def load_sound(filename, sound_lvl=1.0):
    path = os.path.join('data', 'sound', filename)
    sound = pygame.mixer.Sound(path)
    sound.set_volume(sound_lvl)  # Настройка громкости звука
    return sound


COUNT_LASER = 50
NUMBER_NIK = 2
LENGTH_LASER = 50
WIDTH_LASER = 50
INIT_ENERGY = 100
LENGTH_DROID = 50
WIDTH_DROID = 50
LENGTH_SPACESHIP = 32
WIDTH_SPACESHIP = 64
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

# Настроить звуки
intro_sound = load_sound('intro.ogg', 0.3)
explosion_sound = load_sound('explosion_explosion.ogg', 0.3)
energy_sound = load_sound('energy.ogg', 0.3)
game_over_sound = load_sound('game_over.ogg', 1.0)
game_won_sound = load_sound('game_won.ogg', 1.0)
laser_droid_sound = load_sound("laser_droid.ogg", 0.3)
laser_player_sound = load_sound('laser_player.ogg', 0.3)
explosion_player = load_sound("explosion_player.ogg", 0.3)
explosion_droid = load_sound("explosion_droid.ogg", 0.3)
explosion_asteroid = load_sound("destroyed_asteroid.ogg", 0.3)

music_channel = pygame.mixer.Channel(4)
music_channel.play(intro_sound, loops=-1, maxtime=0, fade_ms=0)
