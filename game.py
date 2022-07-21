# coding=utf-8

# //////////////////
# ФАЙЛ СОБЫТИЙ ИГРЫ
# //////////////////

import time
from sprites import *
from os import *
import sys
from image import load_image
import sqlite3


count_laser = COUNT_LASER_BAR  # Получаем количество выстрелов лазера игрока


def show_energy_bar(energy):  # Функция отрисовки шкалы энергии
    color = 2.55 * energy

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -1 * energy))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110), 2)


def show_laser_bar(laser):  # Функция отрисовки шкалы количества пуль
    color = 5.1 * laser

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -1 * laser * 2))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110), 2)


def draw_text(text, source, surface, x, y):
    # Временный объект, используемый только для получения прямоугольника (text_obj.get_rect())
    text_object = source.render(text, True, TEXT_COLOR)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(source.render(text, True, TEXT_COLOR), text_rect)


def show_game_result(points):  # Функция отображения результатов уровня
    global destroyed_enemy_counter, game_challenge, lvl, count_laser, index_nick, score_top

    # Если мы выполнили норму уровня по количеству убитых дроидов, то мы выйграли
    if destroyed_enemy_counter >= game_challenge:
        sound = game_won_sound  # Музыка для победы
        img = load_image(path.join('static', 'img', 'background', 'game_won.jpg'), True, DISPLAYMODE)  # Получаем фон
        lvl += 1  # Увеличиваем уровень
        game_challenge += 5  # Увеличиваем задачу на следующий уровень
    else:
        sound = game_over_sound  # Музыка для проигрыша
        img = load_image(path.join('static', 'img', 'background', 'game_lost.jpg'), True, DISPLAYMODE)  # Получаем фон
        lvl = 1  # Обнуляем уровень до 1
        game_challenge = 3  # Устонавливаем задачу для 1 уровня
    destroyed_enemy_counter = 0  # Обнуляем количество убитых на текущем уровне
    new_data(lvl, game_challenge, index_nick, score_top, destroyed_enemy_counter)  # Вносим изменения в базу данных
    window.blit(img, (0, 0))  # Устанавливаю новый фон
    # Выводим результат игрока на экран
    draw_text(str(points), font_2, window, (WINDOW_WIDTH / 2) - 20, (WINDOW_HEIGHT / 2) - 20)
    pygame.display.update()
    music_channel.play(sound, loops=0, maxtime=0, fade_ms=0)  # Включаем музыку


def exit_game():  # Функция выхода из игры
    pygame.quit()
    sys.exit()


def pause_game():  # Функция паузы
    pause = True
    # Пока пользователь не нажмет на кнопку P, он не выйдет из паузы
    # Но пользователь может выйти из игры
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Нажав клавишу esc, мы выходим из игры
                    exit_game()
                if event.key == pygame.K_p:
                    pause = False

        draw_text("PAUSE", font_1, window, (WINDOW_WIDTH / 2) - 50, (WINDOW_HEIGHT / 2))
        pygame.display.update()


def wait_for_keystroke():  # Функция клавиш для выйгрыша и проигрыша
    # Пользователь не начнет игру, пока не нажмет на BACK
    # Но пользователь может выйти из игры
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                    exit_game()
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_SPACE:
                    return


def wait_for_keystroke_menu():  # Функция клавиш главного меню
    # Пользователь не начнет игру, пока не нажмет на SPACE
    # Но пользователь может выйти из игры
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                    exit_game()
                if event.key == pygame.K_SPACE:
                    return


def show_help():  # Функция отображения подсказки
    # Получаем фон
    img_help = load_image(path.join('static', 'img', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    window.blit(img_help, (0, 0))  # Устанавливаю фон
    pygame.display.update()
    wait_for_keystroke()  # Мы не выйдем из цикла, пока не нажмем любую клавишу


def show_list_nick():  # Функция смены ника
    global index_nick
    # Получаем фон
    img_nick = load_image(path.join('static', 'img', 'background', 'background_nick.jpg'), True, DISPLAYMODE)
    window.blit(img_nick, (0, 0))  # Устанавливаю фон
    list_nick = []
    for j in range(NUMBER_NIK):  # Загружаем картинки ников для выбора
        path_image = os.path.join('static', 'img', 'spaceship', str(j + 1), "spaceship_3.png")
        list_nick.append(load_image(path_image, False, (LENGTH_SPACESHIP, WIDTH_SPACESHIP)))
        image_nick = list_nick[j]
        window.blit(image_nick, (150 * (j + 1), 150))
    pygame.display.update()
    # Пользователь не начнет игру, пока не нажмет на BACK
    # Но пользователь может выйти из игры
    # Может выбрать ник нажав на цифру порядкового номера ника
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                    exit_game()
                if event.key == pygame.K_BACKSPACE:
                    return
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_1]:
            index_nick = 1  # Устанавливаю новый ник
            return update_player(index_nick)  # Получаю изменения
        if key_pressed[pygame.K_2]:
            index_nick = 2  # Устанавливаю новый ник
            return update_player(index_nick)  # Получаю изменения


def update_player(index):  # Функция обновления спрайтов
    player = Player(index)
    group_laser_player = pygame.sprite.RenderUpdates()
    player_team = pygame.sprite.RenderUpdates(player)
    enemy_team = pygame.sprite.RenderUpdates()
    return player, group_laser_player, player_team, enemy_team


def new_game():  # Функция меню игры при первом входе и сбросе на новую игру
    pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=4096)  # Настраиваем музыку
    music_channel.play(intro_sound, loops=-1, maxtime=0, fade_ms=0)  # Включаем музыку
    pygame.display.set_caption("Star Wars")
    # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)   # Развертывание на полный экран
    # Фоновое изображение
    background = load_image(path.join('static', 'img', 'background', 'background_1.jpg'), True, DISPLAYMODE)
    window.blit(background, (0, 0))
    pygame.mouse.set_visible(False)  # Прячем мышку на поле
    pygame.display.update()
    wait_for_keystroke_menu()  # Клавиши
    music_channel.stop()  # Остонавливаем музыку


def new_data(l, challenge, nick, score, destroyed_enemy):  # Функция сохранения новых значений в базу данных
    global count_laser
    count_laser = COUNT_LASER_BAR
    con = sqlite3.connect(path.join('db', 'player data.db'))
    cur = con.cursor()
    cur.execute("""INSERT INTO game (lvl, challenge, index_nick, score, destroyed_enemy_counter)
                VALUES(?, ?, ?, ?, ?)""", (l, challenge, nick, score, destroyed_enemy))
    con.commit()
    con.close()


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        new_game()  # Отображаем меню
        self.time = pygame.time.Clock()  # Создаем объект времени

    def run(self):
        global destroyed_enemy_counter, count_laser, index_nick, lvl, game_challenge, score_top
        con = sqlite3.connect(path.join('db', 'player data.db'))
        cur = con.cursor()
        result = cur.execute('''SELECT lvl, challenge, index_nick, score, destroyed_enemy_counter FROM game
                                    WHERE ID = (SELECT MAX(ID) FROM game)''')  # Забираем последние данные из базы
        lvl = 1
        game_challenge = 5
        index_nick = 1
        score_top = 0
        destroyed_enemy_counter = 0

        for elem in result:
            lvl = elem[0]  # Текущий уровень
            game_challenge = elem[1]  # Количество дронов которых необходимо убить
            index_nick = elem[2]  # Индекс ника
            score_top = elem[3]  # Лучший счет
            destroyed_enemy_counter = elem[4]  # Количество уничтоженых дроидов
        con.commit()
        con.close()
        # Начальные данные игры
        delay_laser = 0
        fps_laser = 0
        time_elapsed = time.clock()

        while True:  # Цикл уровня
            if not time.clock():
                start_time = time.perf_counter()
            else:
                start_time = time.clock()

            enemy_creation_period = 2  # Период за который энергия начинает возобновляться
            energy = INIT_ENERGY  # Получаем количество энергии
            points = 0  # Счет
            counter_asteroid = 0  # Количество

            # Настраиваем игрока и врага
            player, group_laser_player, player_team, enemy_team = update_player(index_nick)
            for _ in range(3):  # Первые 3 дроида в уровне
                enemy_team.add(Enemy())
            group_asteroids = pygame.sprite.RenderUpdates()  # Астероиды
            group_energy = pygame.sprite.RenderUpdates()  # Энергия
            group_explosion = pygame.sprite.RenderUpdates()  # Взрывы

            # Фоновое изображение
            background_game = load_image(path.join('static', 'img', 'background', 'background_2.jpg'),
                                         True, DISPLAYMODE)

            # Меню игрока
            energy_box = TextBox("Жизненная энергия: {}".format(energy), font_1, (10, 80))  # Энергия
            score_top_box = TextBox("Лучший счет: {}".format(score_top), font_1, (10, 120))  # Лучший счет
            # Количество уничтоженных дроидов
            objectives_box = TextBox("Вы уничтожили: {} дроидов".format(destroyed_enemy_counter), font_1, (10, 160))
            challenge_box = TextBox("Осталось: {} дроидов".format(game_challenge - destroyed_enemy_counter),
                                    font_1, (10, 200))  # Количество оставшихся дроидов
            time_box = TextBox("Время: {0:.2f}".format(start_time), font_1, (10, 240))  # Время
            points_box = TextBox("Счёт: {}".format(points), font_1, (10, 280))  # Счет
            lvl_box = TextBox("Уровень: {}".format(lvl), font_1, (10, 320))  # Уровень
            group_box = pygame.sprite.RenderUpdates(points_box, score_top_box, objectives_box, challenge_box,
                                                    time_box, energy_box, lvl_box)

            counter_loop = 0
            check_on_press_keys = True
            while True:  # Цикл действий игры
                # Отрисовываем задний фон
                window.blit(background_game, (0, 0))
                # После проигрыша доступ к клавишам ограничивается
                if check_on_press_keys:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # Выход
                            exit_game()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_F1:  # Помошь
                                show_help()
                                # Отнимаю время, которое пользователь находился в паузе
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_F2:  # Смена ника
                                player.kill()
                                player, group_laser_player, player_team, enemy_team = show_list_nick()
                                # Отнимаю время, которое пользователь находился в паузе
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_p:  # Пауза
                                pause_game()
                                # Отнимаю время, которое пользователь находился в паузе
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_n:  # Новая игра
                                # Обнуляем и сохраняем данные, удаляем врагов
                                lvl, game_challenge,  index_nick, score_top, destroyed_enemy_counter = 1, 3, 1, 0, 0
                                new_data(lvl, game_challenge,  index_nick, score_top, destroyed_enemy_counter)
                                new_game()
                            if event.key == pygame.K_SPACE:  # При каждом нажатии убираем задержку выстрела
                                delay_laser = 9
                        elif event.type == pygame.KEYUP:
                            # Постоянно обнуляем, иначе будет ездить туда сюда =)
                            player.x_speed, player.y_speed = 0, 0

                    # Меняем положение игрок в соответствии с нажатыми клавишами
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
                        player.x_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
                        player.x_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
                        player.y_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
                        player.y_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_SPACE]:  # Стреляем
                        delay_laser += 1  # Увеличиваем задержку
                        fps_laser = 0  # Обнуляем fps (количество кадров в секунду для выстрела)
                        if delay_laser == 10 and count_laser - 1 > 0:
                            group_laser_player.add(PlayerLaser(player.rect.midtop))  # Добавляем выстрел в группу
                            delay_laser = 0  # Обнуляем задержку
                            count_laser -= 1  # Уменьшаем количество выстрелов
                    else:
                        fps_laser += 1  # Увеличиваем fps (количество кадров в секунду для выстрела)
                        if fps_laser == 25 and count_laser < COUNT_LASER_BAR:  # Это сделано для плавного выстрелов
                            count_laser += 1  # Увеличиваем количество выстрелов
                            fps_laser = 0  # Обнуляем fps (количество кадров в секунду для выстрела)

                else:  # Мы входим в блок сразу после того, как энергия заканчивается
                    # (ЗАДЕРЖКА * 6 - количество изображений анимации) + еще 20 циклов, чтобы иметь момент паузы
                    total_loops = (DELAY * 6) + 20
                    if counter_loop == total_loops:
                        break  # Выходим во внешний цикл
                    counter_loop += 1  # Увеличиваем счетчик
                counter_asteroid += 1  # Увеличиваем счетчик астероида
                if counter_asteroid == ADD_NEW_ASTEROID_RATE:  # Когда счетчик станет равен,
                    # то мы создаем один новый асероида
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

                # Смерть персонажа. Мы проверяем, что это сделано один раз
                if energy == 0 and check_on_press_keys:
                    explosion_player.play()
                    check_on_press_keys = False  # Чтобы отключить ввод нажатий клавиш
                    group_explosion.add(Explosion(player.rect))
                    player.kill()  # Мы убиваем персонажа
                # Игрок выигрывает
                elif destroyed_enemy_counter >= game_challenge:
                    player.kill()
                    break

                # =========================
                # СПРАЙТ СТОЛКНОВЕНИЯ
                # =========================

                # Урон, нанесенный врагом игроку
                for player in pygame.sprite.groupcollide(player_team, group_laser_enemy, False, True):
                    energy -= 15
                # Лазер уничтожает вражеский корабль
                for droid in pygame.sprite.groupcollide(enemy_team, group_laser_player, True, True):
                    points += 15
                    group_explosion.add(Explosion(droid.rect, "explosion"))  # Исчезает во взрыве
                    explosion_droid.play()
                    destroyed_enemy_counter += 1
                # Лазер уничтожает астероиды
                for asteroid in pygame.sprite.groupcollide(group_asteroids, group_laser_player, False, True):
                    points += 5
                    group_explosion.add(Explosion(asteroid.rect, "smoke"))  # Исчезает в облаке дыма
                    explosion_asteroid.play()
                    # Мы спрашиваем, является ли это астероидом (астероид дает энергию для изменения изображения)
                    if asteroid.is_energetic:
                        asteroid.image = asteroid.select_image(path.join('resources', 'energy.png'), True)
                        asteroid.x_speed = 0  # Падать вертикально
                        asteroid.y_speed = 2  # Чтобы замедлить
                        group_energy.add(asteroid)
                        group_asteroids.remove(asteroid)
                    else:
                        asteroid.kill()
                # Когда астероид попадает на корабль
                for asteroid in pygame.sprite.groupcollide(group_asteroids, player_team, True, False):
                    energy -= 10  # Уменьшить энергию, которую имеет корабль
                    group_explosion.add(Explosion(asteroid.rect, "smoke"))
                    explosion_asteroid.play()
                # Когда дроид попадает на корабль
                for droid in pygame.sprite.groupcollide(enemy_team, player_team, True, False):
                    energy -= 10  # Уменьшить энергию, которую имеет корабль
                    group_explosion.add(Explosion(droid.rect, "explosion"))
                    explosion_droid.play()
                # Когда мы прикасаемся к энергии
                for e in pygame.sprite.groupcollide(group_energy, player_team, True, False):
                    energy += e.energy_lvl  # Пополняем энергию игрока
                    energy_sound.play()

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
                player_team.clear(window, background_game)
                group_laser_player.clear(window, background_game)
                enemy_team.clear(window, background_game)
                group_laser_enemy.clear(window, background_game)
                group_asteroids.clear(window, background_game)
                group_energy.clear(window, background_game)
                group_box.clear(window, background_game)
                group_explosion.clear(window, background_game)
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
                points_box.text = "Счёт: {}".format(points)
                score_top_box.text = "Лучший счет: {}".format(score_top)
                objectives_box.text = "Вы уничтожили: {} дроидов".format(destroyed_enemy_counter)
                challenge_box.text = "Осталось: {} дроидов".format(game_challenge - destroyed_enemy_counter)
                time_box.text = "Время: %.2f" % time_elapsed
                lvl_box.text = "Уровень: {}".format(lvl)

                if energy < 0:
                    energy = 0
                elif energy > 100:
                    energy = 100
                show_energy_bar(energy)
                show_laser_bar(count_laser)

                pygame.display.update()
                self.time.tick(FPS)

            # Мы печатаем счет
            if points > score_top:  # Мы проверяем, превышает ли он лучший результат
                score_top = points
            show_game_result(points)
            wait_for_keystroke()
