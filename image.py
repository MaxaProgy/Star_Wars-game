# coding=utf-8

# //////////////////////////
# ФАЙЛ ЗАГРУЗКИ ИЗОБРАЖЕНИЯ
# //////////////////////////

import pygame


def load_image(path, use_transparency=False, rect_img=(0, 0)):
    width, height = rect_img  # Получаю размеры изображения (которые нужно установить)
    try:
        image = pygame.image.load(path)  # Загрузка изображения
    except pygame.error:
        raise SystemExit
    if use_transparency:
        image = image.convert()
    else:  # Проверяем и добавляем прозрачность
        image = image.convert_alpha()
    if width >= 1 and height >= 1:  # Масштабировать изображение до указанного размера
        image = pygame.transform.scale(image, (width, height))
    return image
