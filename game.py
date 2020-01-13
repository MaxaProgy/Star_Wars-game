from os import path
import pygame
import sys
import time
from image import load_image
from pygame.locals import *
from sprites import *
from const import *

# Задача игры - уничтожить 100 врагов
GAME_CHALLENGE = 100


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        pygame.display.set_caption("Star Wars")
        self.time = pygame.time.Clock()
        pygame.mouse.set_visible(False)  # Прячем мышку на поле
        # Соединяем путь к логотипу (с учётом особенностей операционной системы).
        # Отображаем на экране
        logo = load_image(path.join('data', 'images', 'background', 'start_logo.png'))
        self.draw_text("Нажмите клавишу для запуска", font_1, window, (WINDOW_WIDTH / 5), (WINDOW_HEIGHT / 3) + 100)
        window.blit(logo, (150, 100))
        pygame.display.update()
        
        self.wait_for_keystroke()

    def run(self):
        global player, GAME_CHALLENGE
        score_top = 0

        while True:
            if not time.clock():
                start_time = time.perf_counter()
            else:
                start_time = time.clock()

            enemy_creation_period = 2
            energy = INIT_ENERGY
            points = 0
            counter_asteroid = 0

            # Меню игрока
            energy_box = TextBox("Жизненная энергия: {}".format(energy), font_1, 10, 0)
            score_top_box = TextBox("Лучший счет: {}".format(score_top), font_1, 10, 40)
            objectives_box = TextBox("Задача: {}".format(GAME_CHALLENGE), font_1, 10, 80)
            time_box = TextBox("Время: {0:.2f}".format(start_time), font_1, 10, 120)
            points_box = TextBox("Точки: {}".format(points), font_1, 10, 160)
            info_box = TextBox("Нажмите: ESC-Выход из игры     F1-Справка", font_1, 10, WINDOW_HEIGHT - 40)
            group_box = pygame.sprite.RenderUpdates(points_box, score_top_box, objectives_box,
                                                    time_box, energy_box, info_box)

            counter_loop = 0
            check_on_press_keys = True
            while True:
                # Отрисовываем задний фон
                window.blit(background, (0, 0))
                # После проигрыша доступ к клавишам ограничивается
                if check_on_press_keys:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.exit_game()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_F1:
                                self.show_help()
                            if event.key == pygame.K_p:
                                self.pause_game()
                            if event.key == pygame.K_ESCAPE:
                                self.exit_game()
                            if event.key == pygame.K_SPACE:
                                group_laser_player.add(PlayerLaser(player.rect.midtop))
                        elif event.type == pygame.KEYUP:
                            player.x_speed, player.y_speed = 0, 0

                    # Перемещение игрока в пространстве(на экране)
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_LEFT]:
                        player.x_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_RIGHT]:
                        player.x_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_UP]:
                        player.y_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_DOWN]:
                        player.y_speed = RATE_PLAYER_SPEED
                else:  # Мы входим в блок сразу после того, как энергия заканчивается
                    # (ЗАДЕРЖКА * 6 - количество изображений анимации) + еще 20 циклов, чтобы иметь момент паузы
                    total_loops = (DELAY_EXPLOSION * 6) + 20
                    if counter_loop == total_loops:
                        break  # Мы оставили левый цикл
                    counter_loop += 1  # Увеличиваем счетчик
                counter_asteroid += 1
                if counter_asteroid == ADDNEW_ASTEROID_RATE:
                    counter_asteroid = 0
                    group_asteroids.add(Asteroid())

                # Создайте вражеских дроидов
                # Служит для добавления дроидов всякий раз, когда его значение больше или равно 500
                # Затем он сбрасывается. Нельзя насильно добавлять дроидов
                enemy_creation_period += 12

                if len(enemy_team) <= MAX_NUMBER_DROIDS:
                    # Мы ограничиваем максимальное количество дроидов, которые будут созданы
                    if enemy_creation_period >= 450:
                        enemy_creation_period = 0
                        enemy_team.add(Enemy())
                    elif enemy_creation_period == 210:
                        for _ in range(2):
                            enemy_team.add(Enemy())
                    elif enemy_creation_period == 50:
                        for _ in range(3):
                            enemy_team.add(Enemy())

                # Считаем время
                if not time.clock():
                    time_current = time.perf_counter()
                else:
                    time_current = time.clock()
                # Устонавливаем конечное время
                time_elapsed = time_current - start_time
                time_elapsed = time_elapsed * 2

                # Смерть персонажа. Мы проверяем, что это сделано один раз
                if energy <= 0 and check_on_press_keys:
                    if points > score_top: # Мы проверяем, превышает ли он лучший результат
                        score_top = points
                    check_on_press_keys = False  # Чтобы отключить ввод нажатий клавиш
                    group_explosion.add(Explosion(player.rect))
                    player.kill()  # Мы убиваем персонажа
                    loop_counter = 0
                # Победить персонажа
                elif GAME_CHALLENGE <= 0:
                    if points > score_top:  # Мы проверяем, превышает ли он лучший результат
                        score_top = points
                    check_on_press_keys = False  # Чтобы отключить ввод нажатий клавиш
                    player.kill()
                    loop_counter = 0
                    break
# =========================
# СПРАЙТ СТОЛКНОВЕНИЯ
# =========================
                # Урон, нанесенный врагом игроку
                for player in pygame.sprite.groupcollide(player_team, group_laser_enemy, False, True):
                    energy = energy - 5
                # Лазер уничтожает вражеский корабль
                for droid in pygame.sprite.groupcollide(enemy_team, group_laser_player, True, True):
                    points += 15
                    group_explosion.add(Explosion(droid.rect, "explosion"))  # Исчезает во взрыве
                    GAME_CHALLENGE -= 1
                # Лазер уничтожает астероиды
                for asteroid in pygame.sprite.groupcollide(group_asteroids, group_laser_player, False, True):
                    points += 5
                    group_explosion.add(Explosion(asteroid.rect, "smoke"))  # Исчезает в облаке дыма
                    # Мы спрашиваем, является ли это астероидом (астероид дает энергию для изменения изображения)
                    if asteroid.is_energetic:
                        asteroid.image = asteroid.select_image( path.join('resources', 'energy.png'), True)
                        asteroid.x_speed = 0  # Падать вертикально
                        asteroid.y_speed = 2  # Чтобы замедлить
                        group_energy.add(asteroid)
                        group_asteroids.remove(asteroid)
                    else:
                        asteroid.kill()
                # Когда астероид попадает на корабль
                for asteroid in pygame.sprite.groupcollide(group_asteroids, player_team, True, False):
                    energy = energy - 7  # Уменьшить энергию, которую имеет корабль
                    group_explosion.add(Explosion(asteroid.rect, "smoke"))
                # Когда дроид попадает на корабль
                for droid in pygame.sprite.groupcollide(enemy_team, player_team, True, False):
                    energy = energy - 7  # Уменьшить энергию, которую имеет корабль
                    group_explosion.add(Explosion(droid.rect, "explosion"))
                # Когда мы прикасаемся к энергии
                for e in pygame.sprite.groupcollide(group_energy, player_team, True, False):
                    if energy < 100:
                        energy += e.energy_lvl  # Пополняем энергию игрока
                        if energy >= 100:
                            energy = 100
# =============================
# ОБНОВЛЯЕМ ВСЕ ГРУППЫ
# =============================
                player_team.update()
                group_laser_player.update()
                enemy_team.update()
                group_laser_enemy.update()
                group_asteroids.update()
                group_energy.update()
                group_box.update()
                group_explosion.update()
# =======================
# ОЧИЩАЕМ СПРАЙТЫ
# =======================
                player_team.clear(window, background)
                group_laser_player.clear(window, background)
                enemy_team.clear(window, background)
                group_laser_enemy.clear(window, background)
                group_asteroids.clear(window, background)
                group_energy.clear(window, background)
                group_box.clear(window, background)
                group_explosion.clear(window, background)
                player_team.draw(window)
                group_laser_player.draw(window)
                enemy_team.draw(window)
                group_laser_enemy.draw(window)
                group_asteroids.draw(window)
                group_energy.draw(window)
                group_box.draw(window)
                group_explosion.draw(window)

                # Вносим новые значения в меню игрока
                energy_box.text = "Энергия: {0}%".format(int(energy))
                points_box.text = "Точки: {}".format(points)
                score_top_box.text = "Лучший счет: {}".format(score_top)
                objectives_box.text = "Осталось убить : {} дроидов".format(GAME_CHALLENGE)
                time_box.text = "Время: %.2f" % time_elapsed
                info_box.text = "Press: ESC-Exit     F1-Help"

                pygame.display.update()
                self.time.tick(FPS)

            # Мы печатаем счет
            self.show_game_result(points)
            time_lapse = 4000  # 4 sec
            pygame.time.delay(time_lapse)
            self.wait_for_keystroke()

    def draw_text(self, text, source, surface, x, y):
        # Временный объект, используемый только для получения прямоугольника (text_obj.get_rect ())
        text_object = source.render(text, True, TEXTCOLOR)
        text_rect = text_object.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(source.render(text, True, TEXTCOLOR), text_rect)


    def show_help(self):
        img_help = load_image(path.join('data', 'images', 'background', 'help.jpg'), True, DISPLAYMODE)
        window.blit(img_help, (0, 0))  # Изображение для покрытия фона
        pygame.display.update()  # Мы рисуем весь экран, чтобы стереть предыдущее изображение
        self.draw_text('Нажмите клавишу, чтобы возобновить игру',
                       font_1, window, (WINDOW_WIDTH / 3), WINDOW_HEIGHT - 20)
        pygame.display.update()
        self.wait_for_keystroke()  # Мы не выйдем из цикла, пока не нажмем любую клавишу

    def show_game_result(self, points):
        if GAME_CHALLENGE <= 0:
            image = load_image(path.join('data', 'images', 'background', 'game_won.jpg'), True, DISPLAYMODE)
        else:
            image = load_image(path.join('data', 'images', 'background', 'game_lost.jpg'), True, DISPLAYMODE)
        window.blit(image, (0, 0))
        pygame.display.update()
        self.draw_text(str(points), font_5, window, (WINDOW_WIDTH / 2) - 20, (WINDOW_HEIGHT / 2) - 20)
        pygame.display.update()

    def wait_for_keystroke(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                        self.exit_game()
                    return  # Нажав любую клавишу мы уходим и игра начинается

    def pause_game(self):
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Нажав клавишу esc, мы выходим из игры

                        self.exit_game()
                    if event.key == pygame.K_p:
                        pause = False
            self.draw_text("PAUSE", font_5, window, (WINDOW_WIDTH / 2) - 50, (WINDOW_HEIGHT / 2))
            pygame.display.update()

    def exit_game(self):
        pygame.quit()
        sys.exit()