# coding=utf-8

# //////////////////
# ФАЙЛ СПРАЙТОВ
# //////////////////

import random
from const import *
from image import load_image


# =========================
# СПРАЙТ ИГРОКА
# =========================

class Player(pygame.sprite.Sprite):
    def __init__(self, index_nik):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров игрока определенного размера LENGTH_SPACESHIP, WIDTH_SPACESHIP (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.list_spaceship = [load_image(
            os.path.join('static', 'img', 'spaceship', str(index_nik),  "spaceship_" + str(i + 1) + '.png'),
            False, (LENGTH_SPACESHIP, WIDTH_SPACESHIP)) for i in range(COUNT_PLAYER)]

        # Индекс текущего изображения игрока и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0
        self.image = self.list_spaceship[self.index]  # Устанавливаю старовое изображение

        # Получаю размеры изображения, квадрат
        # (Для проверок на сталкновения и расположение игрока на экране)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT)  # Стартовое расположение игрока на экране
        self.x_speed, self.y_speed = 0, 0  # Скорость игрока по x и y (начальная)

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1  # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения
            if self.index < len(self.list_spaceship):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_spaceship[self.index]
            else:
                # Индекса нет в длине списка изображений, меняем индекс на начальный
                self.index = -1

        # Меняем положение игрока в соответствии с установленным
        self.rect.move_ip((self.x_speed, self.y_speed))

        # Проверяем на выход за границы экрана
        if self.rect.left < 250:
            self.rect.left = 250
        elif self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        # Проверка на превышение половины экрана (вверх можем только до половины экрана двигаться)
        if self.rect.top <= WINDOW_HEIGHT / 2:
            self.rect.top = WINDOW_HEIGHT / 2
        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT


# =========================
# СПРАЙТ ВРАГА
# =========================

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров врага определенного размера LENGTH_DROID, WIDTH_DROID (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.list_droid = [load_image(
            os.path.join('static', 'img', 'droid', "droid_" + str(i + 1) + '.png'),
            False, (LENGTH_DROID, WIDTH_DROID)) for i in range(COUNT_DROID)]

        # Индекс текущего изображения врага и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0

        self.image = self.list_droid[self.index]  # Устанавливаю старовое изображение
        # Получаю размеры изображения, квадрат
        # (Для проверок на сталкновения и расположение врага на экране)
        self.rect = self.image.get_rect()

        # Случайное расположение врага на экране
        self.rect.center = (random.randint(260, 752), random.randint(60, 230))
        self.x_speed, self.y_speed = random.randint(-7, 7), random.randint(-7, 7)  # Скорость врага по x и y (начальная)

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1  # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения

            if self.index < len(self.list_droid):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_droid[self.index]
            else:
                # Индекса нет в длине списка изображений, меняем индекс на начальный
                self.index = -1

        # Меняем положение врага в соответствии с установленным
        self.rect.move_ip((self.x_speed, self.y_speed))

        # Проверяем на выход за границы экрана
        if self.rect.left <= 250 or self.rect.right >= WINDOW_WIDTH:
            self.x_speed = -self.x_speed
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT / 2:
            self.y_speed = -self.y_speed

        # Если случайное число равно 1. Это мешает вражескому кораблю все время стрелять
        if random.randint(1, 80) == 1:  # Дроид стреляет, только если разрешено
            group_laser_enemy.add(LaserEnemy(self.rect.midbottom))
            laser_droid_sound.play()  # Создаем лазер


# =========================
# СПРАЙТ АСТЕРОИДА
# =========================

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.energy_lvl = 10  # Уровень энергии, которая дается астероидом
        self.is_energetic = (random.random() < PROB_ENERGETIC_ASTEROID)  # Определяем дает ли текущий астероид энергию
        if self.is_energetic:
            # Получаю изображение астероида с энергией
            self.image = self.select_image(os.path.join("resources", "energetic_asteroid.png"))
        else:
            # Получаю изображение обычного астероида
            self.image = self.select_image(os.path.join("resources", "asteroid.png"))

        # Получаю размеры изображения, квадрат
        # (Для проверок на сталкновения и расположение астероида на экране)
        self.rect = pygame.Rect(random.randint(0, WINDOW_WIDTH - LENGTH_ASTEROID),
                                0 - WIDTH_ASTEROID, LENGTH_ASTEROID, WIDTH_ASTEROID)

        self.rect.center = (random.randint(260, WINDOW_WIDTH), 0)  # Начальное положение астероила
        # Скорость астероида по x и y (начальная)
        self.x_speed = random.randint(-ASTEROID_MAX_SPEED, ASTEROID_MAX_SPEED)
        self.y_speed = random.randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)

    def update(self):
        # Меняем положение астероида в соответствии с установленным
        self.rect.move_ip(self.x_speed, self.y_speed)

        # Проверяем на выход за границы экрана
        if self.rect.left <= 250 or self.rect.right >= WINDOW_WIDTH or self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()

    def select_image(self, archive, is_energy=False):
        path_img = os.path.join('static', 'img', archive)
        if is_energy:  # Мы спрашиваем, стоит ли менять изображение на энергию
            image = load_image(path_img, False, (LENGTH_ENERGY, WIDTH_ENERGY))
        else:  # Изображение любого метеорита
            image = load_image(path_img, False, (LENGTH_ASTEROID, WIDTH_ASTEROID))
        return image


# =========================
# СПРАЙТ ЛАЗЕРА ИГРОКА
# =========================

class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, coordinate):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров лазера игрока определенного размера LENGTH_LASER, WIDTH_LASER (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.list_laser = [load_image(
            os.path.join('static', 'img', 'player_laser', "laser_player_" + str(i + 1) + '.png'),
            False, (LENGTH_LASER, WIDTH_LASER)) for i in range(COUNT_LASER)]

        # Индекс текущего изображения лазера игрока и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0

        self.image = self.list_laser[self.index]  # Устанавливаю старовое изображение

        # Получаю размеры изображения, квадрат
        # (Для проверок на сталкновения и расположение лазера игрока на экране)
        self.rect = self.image.get_rect()
        self.rect.center = coordinate  # Стартовое расположение игрока на экране

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1  # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения
            if self.index < len(self.list_laser):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_laser[self.index]
            else:
                # Индекса нет в длине списка изображений, меняем индекс на начальный
                self.index = -1

        # Проверяем на выход за границы экрана
        if self.rect.bottom >= 0:
            self.rect.move_ip((0, -10))  # Меняем положение лазера игрока
        else:
            self.kill()


# =========================
# СПРАЙТ ЛАЗЕРА ВРАГА
# =========================

class LaserEnemy(pygame.sprite.Sprite):
    def __init__(self, coordinate):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров лазера врага определенного размера LENGTH_LASER, WIDTH_LASER (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.list_laser = [load_image(
            os.path.join('static', 'img', 'enemy_laser', "laser_enemy_" + str(i + 1) + '.png'),
            False, (LENGTH_LASER, WIDTH_LASER)) for i in range(COUNT_LASER)]

        # Индекс текущего изображения лазера врага и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0

        self.image = self.list_laser[self.index]  # Устанавливаю старовое изображение
        # Получаю размеры изображения, квадрат
        # (Для проверок на сталкновения и расположение лазера врага на экране)
        self.rect = self.image.get_rect()
        self.rect.center = coordinate  # Стартовое расположение игрока на экране

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1  # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения
            if self.index < len(self.list_laser):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_laser[self.index]
            else:
                # Индекса нет в длине списка изображений, меняем индекс на начальный
                self.index = -1

        # Проверяем на выход за границы экрана
        if self.rect.bottom <= WINDOW_HEIGHT:
            self.rect.move_ip((0, 6))
        else:
            self.kill()


# =========================
# СПРАЙТ МЕНЮ ИГРОКА
# =========================

class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, font, coordinate):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.text = text
        self.image = self.font.render(self.text, True, TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coordinate

    def update(self):
        self.image = self.font.render(self.text, True, TEXT_COLOR)


# =========================
# СПРАЙТ ВЗРЫВА
# =========================

class Explosion(pygame.sprite.Sprite):
    def __init__(self, object_rect, type_explosion="explosion"):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров взрыва определенного размера WIDTH_EXPLOSION, LENGTH_EXPLOSION (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.sp_image_explosion = [load_image(
            os.path.join('static', 'img', 'animation', type_explosion + str(i + 1) + '.png'),
            False, object_rect.size) for i in range(COUNT_EXPLOSION)]

        # Индекс текущего изображения взрыва и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0
        self.image = self.sp_image_explosion[self.index]  # Устанавливаю старовое изображение
        # Получаю размеры изображения, квадрат
        self.rect = self.image.get_rect()
        # Стартовое расположение взрыва на экране равно расположению предмета до взрыва
        self.rect.x, self.rect.y = object_rect.x, object_rect.y

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1   # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения
            if self.index < len(self.sp_image_explosion):   # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.sp_image_explosion[self.index]
            else:
                # Индекса нет в длине списка изображений, значит удаляем объект
                self.kill()


group_laser_enemy = pygame.sprite.RenderUpdates()  # Создаю группу пуль врага
