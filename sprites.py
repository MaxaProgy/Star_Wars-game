import os
import random
from image import load_image
from const import *


# =========================
# СПРАЙТ ИГРОКА
# =========================


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.list_spaceship = []
        self.index = 0
        self.speed_image = 0
        for i in range(10):  # Загружаем картинки
            path_img = os.path.join('data', 'images', 'spaceship', "spaceship_" + str(i + 1) + '.png')
            self.list_spaceship.append(load_image(path_img, False, (LENGTH_SPACESHIP, WIDTH_SPACESHIP)))

        self.image = self.list_spaceship[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT)
        self.x_speed = 0  # Перемещение по x
        self.y_speed = 0  # Перемещение по y

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_spaceship):  # Отображаем изображение
                self.image = self.list_spaceship[self.index]
            else:
                self.index = 0

        self.rect.move_ip((self.x_speed, self.y_speed))  # Смещение коробля игрока в указанном направлении
        if self.rect.left < 0:  # Проверка на превышение стороны
            self.rect.left = 0
        elif self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        if self.rect.top <= WINDOW_HEIGHT / 2:  # Проверка на превышение половины экрана
            self.rect.top = WINDOW_HEIGHT / 2
        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT


# =========================
# СПРАЙТ ВРАГА
# =========================


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.list_droid = []
        self.index = 0
        self.speed_image = 0
        for i in range(2):  # Загружаем картинки
            path_img = os.path.join('data', 'images', 'droid', "droid_" + str(i + 1) + '.png')
            self.list_droid.append(load_image(path_img, False, (LENGTH_DROID, WIDTH_DROID)))
        self.image = self.list_droid[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT)
        self.x_speed = 0  # Перемещение по x
        self.y_speed = 0  # Перемещение по y

        # Случайное расположение
        self.rect.centerx = random.randint(40, 752)
        self.rect.centery = random.randint(60, 230)
        self.x_speed = random.randint(-5, 5)
        self.y_speed = random.randint(-5, 5)
        if self.x_speed == 0:
            self.x_speed = 1
        elif self.y_speed == 0:
            self.y_speed = 1

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_droid):  # Отображаем изображение
                self.image = self.list_droid[self.index]
            else:
                self.index = 0

        self.rect.move_ip((self.x_speed, self.y_speed))
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.x_speed = -self.x_speed
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT / 2:
            self.y_speed = -self.y_speed
        # is_shoot = True, если случайное число равно 1. Это мешает вражескому кораблю все время стрелять
        is_shoot = random.randint(1, 80) == 1
        if is_shoot:  # Дроид стреляет, только если разрешено
            group_laser_enemy.add(LaserEnemy(self.rect.midbottom))


# =========================
# СПРАЙТ АСТЕРОИДА
# =========================


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size_asteroid = ASTEROID_SIZE
        self.is_energetic = (random.random() < PROB_ENERGETIC_ASTEROID)  # Определяем дает ли текущий астероид энергию
        self.energy_lvl = 0  # Уровень энергии, которая дается астероидом (0 без энергии)
        if self.is_energetic:
            self.image = self.select_image(os.path.join("resources", "energetic_asteroid.png"))
            # Определяем кол-во энергии в зависимости от размера астероида
            if self.size_asteroid == 30:
                self.energy_lvl = 10
        else:
            self.image = self.select_image(os.path.join("resources", "asteroid.png"))
        self.rect = pygame.Rect(random.randint(0, WINDOW_WIDTH - self.size_asteroid),
                                0 - self.size_asteroid, self.size_asteroid, self.size_asteroid)
        self.rect.centerx = random.randint(48, WINDOW_WIDTH)
        self.rect.centery = 0
        self.x_speed = random.randint(-ASTEROID_MAX_SPEED, ASTEROID_MAX_SPEED)
        self.y_speed = random.randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)

    def update(self):
        self.rect.move_ip((self.x_speed, self.y_speed))
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH or self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()

    def select_image(self, archive, is_energy=False):
        path_img = os.path.join('data', 'images', archive)
        if is_energy:  # Мы спрашиваем, стоит ли менять изображение на энергию
            image = load_image(path_img, False, (int(30 / 2), int(30 / 2)))
        else:  # Изображение любого метеорита
            image = load_image(path_img, False, (self.size_asteroid, self.size_asteroid))
        return image


# =========================
# СПРАЙТ ЛАЗЕРА ИГРОКА
# =========================


class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, p):
        pygame.sprite.Sprite.__init__(self)
        self.list_laser = []
        self.index = 0
        self.speed_image = 0
        for i in range(4):  # Загружаем картинки
            path_img = os.path.join('data', 'images', 'player_laser', "laser_player_" + str(i + 1) + '.png')
            self.list_laser.append(load_image(path_img, False, (LENGTH_LASER, WIDTH_LASER)))

        self.image = self.list_laser[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = p

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_laser):  # Отображаем изображение
                self.image = self.list_laser[self.index]
            else:
                self.index = 0

        if self.rect.bottom >= 0:
            self.rect.move_ip((0, -10))
        else:
            self.kill()


# =========================
# СПРАЙТ ЛАЗЕРА ВРАГА
# =========================


class LaserEnemy(pygame.sprite.Sprite):
    def __init__(self, p):
        pygame.sprite.Sprite.__init__(self)
        self.list_laser = []
        self.index = 0
        self.speed_image = 0
        for i in range(4):  # Загружаем картинки
            path_img = os.path.join('data', 'images', 'enemy_laser', "laser_enemy_" + str(i + 1) + '.png')
            self.list_laser.append(load_image(path_img, False, (LENGTH_LASER, WIDTH_LASER)))

        self.image = self.list_laser[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = p

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_laser):  # Отображаем изображение
                self.image = self.list_laser[self.index]
            else:
                self.index = 0
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()
        else:
            self.rect.move_ip((0, 6))


# =========================
# СПРАЙТ МЕНЮ ИГРОКА
# =========================


class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, font, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.text = text
        self.image = self.font.render(self.text, True, TEXTCOLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y

    def update(self):
        self.image = self.font.render(self.text, True, TEXTCOLOR)


# =========================
# СПРАЙТ ВЗРЫВА
# =========================


class Explosion(pygame.sprite.Sprite):
    def __init__(self, object_rect, type_explosion="explosion"):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.speed_image = 0
        quantity_image = 6  # Количество изображений, содержащихся в анимации
        self.sp_image_explosion = []

        for i in range(0, quantity_image):  # Загружаем картинки
            path_img = os.path.join('data', 'images', 'animation', type_explosion + str(i + 1) + '.png')
            self.sp_image_explosion.append(load_image(path_img, False, object_rect.size))

        self.image = self.sp_image_explosion[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = object_rect.x
        self.rect.y = object_rect.y

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.sp_image_explosion):  # Отображаем изображение
                self.image = self.sp_image_explosion[self.index]
            else:  # Или удаляем объект
                self.kill()


# ================================
# Создаем спрайты и группы
# ================================

# Настраиваем игрока
player = Player()
player_team = pygame.sprite.RenderUpdates(player)
group_laser_player = pygame.sprite.RenderUpdates()

# Настраиваем врагов
enemy_team = pygame.sprite.RenderUpdates()
for i in range(3):  # Добавляем 3 врагов
    enemy_team.add(Enemy())
group_laser_enemy = pygame.sprite.RenderUpdates()

# Настраиваем астероиды
group_asteroids = pygame.sprite.RenderUpdates()
group_energy = pygame.sprite.RenderUpdates()

# Мы создаем объект для амитации взрыва
group_explosion = pygame.sprite.RenderUpdates()