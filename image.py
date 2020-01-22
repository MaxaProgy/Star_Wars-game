# coding=utf-8
import pygame


def load_image(path, use_transparency=False, rect_img=(0, 0)):  # Функция загрузки изображений
    width, height = rect_img
    try:  # Загрузка изображения
        image = pygame.image.load(path)
    except pygame.error:
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
