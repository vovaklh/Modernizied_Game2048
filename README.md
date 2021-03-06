# Улучшенная версия игры "2048"
Суть задачи:
1. Реализовать игру с помощью языка программирования **python** и библиотеки **pygame** (сделано)
Игра реализована в двух файлах. В **Logic_2048.py** реализована вся логика игры. В нее входит функции сдвига плиток по всем 4-м направлениям, функции объединения плиток, функция генерации новой плитки и функции, которые проверяют, выиграл или проиграл игрок. В **Interface_2048** реализована отрисовка нашего массива чисел в окне, а также дополнительные функции.

![Результат работы](/Game_2048.png)

2. Сделать возможным управление голосом в игре (сделано)
Реализовано с помощью библиотеки speech_recognition, которая использует API Google. Функции для использования данной возможности реализованы в файле **Interface_2048**. Для корректной работы используются отдельный демонический поток.
3. Добавить возможность управления кистью руки (сделано)
Реализовано с помощью библиотеки компьютерного зрения с открытым кодом **OpenCV**. Код взят с репозитория https://github.com/Jitender46559/AI-Ignition-system Оригинальная часть заключается в определении направления движения. **Алгоритм**: в каждый момент времени добавлять в массив координаты руки. Когда количество координат достигнет числа n, то посчитать дисперсию координат по х и по у. Выбрать ту координату, где дисперсия больше и посчитать разницу между первой и последней и в зависимости от числа(отрицательного или положительного) выбрать направление. Данный алгоритм также работает в отельном потоке.

![Алгоритм направления движения](/hand_detection.png)

4. Добавить в игру бота (сделано)
Бот использует метод Монте-Карло. Чтобы определить следующий ход для данного состояния поля, ИИ разыгрывает в игру в оперативной памяти, делая случайные ходы до тех пор, пока игра не закончится поражением. Это делается несколько раз, при этом отслеживается конечный счет. Затем рассчитывается средний конечный балл с учётом начального хода. В качестве уже реально выбираемого хода выбирается тот начальный ход, который показал наибольший средний результат. Код бота был взят с репозитория Github https://github.com/jiangyangzhou/2048 и адаптирован для моего кода.

![Пример игры бота](/Bot_game.png)

5. Сделать сбор статистики по игре (сделано)
Данная возможность будет реализована с помощью библиотеки **pandas**. На основе собранных данных можно будет проанализировать тактику игрока и создать еще одного бота на основе предыдущих ходов или генерировать новые плитки по какому-то правилу.

![Гистограмма каждого хода игрока](/Statistics.png)

# Использование игры
Данная игра включает обычную возможность управления стрелками. Для того, чтобы включить бота, нажмите "a", для остановки - "q". Для включения голосового помощника нажмите "s". Клавиша "c" позволяет активировать возможность управление рукой, escape отключает эту возможность.
