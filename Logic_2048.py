import random
import numpy as np
import keyboard

Size = 4
score = 0
arr = np.zeros((4, 4)).astype(int)


def new_game():
    global score
    global arr

    arr = np.zeros((4, 4)).astype(int)
    arr[random.randint(0, 1)][random.randint(0, 3)] = 2
    arr[random.randint(2, 3)][random.randint(0, 3)] = 2
    score = 0


def generate():
    list_of_indexes = []

    for i in range(Size):
        for j in range(Size):
            if arr[i, j] == 0 and [i, j] not in list_of_indexes:
                list_of_indexes.append([i, j])

    random_index = random.randint(0, len(list_of_indexes) - 1)
    arr[list_of_indexes[random_index][0]][list_of_indexes[random_index][1]] = 2


def shift_up():
    check = 0
    for k in range(Size):
        for i in range(Size):
            for j in reversed(range(1, Size)):
                if arr[j - 1, i] == 0 and arr[j, i] != 0:
                    arr[j - 1, i] = arr[j, i]
                    arr[j, i] = 0
                    check += 1
    if check > 0:
        return True
    else:
        return False


def shift_down():
    check = 0
    for k in range(Size):
        for i in range(Size):
            for j in range(Size - 1):
                if arr[j + 1, i] == 0 and arr[j, i] != 0:
                    arr[j + 1, i] = arr[j, i]
                    arr[j, i] = 0
                    check += 1
    if check > 0:
        return True
    else:
        return False


def shift_left():
    check = 0
    for k in range(Size):
        for i in range(Size):
            for j in reversed(range(1, Size)):
                if arr[i, j - 1] == 0 and arr[i, j] != 0:
                    arr[i, j - 1] = arr[i, j]
                    arr[i, j] = 0
                    check += 1
    if check > 0:
        return True
    else:
        return False


def shift_right():
    check = 0
    for k in range(Size):
        for i in range(Size):
            for j in range(Size - 1):
                if arr[i, j + 1] == 0 and arr[i, j] != 0:
                    arr[i, j + 1] = arr[i, j]
                    arr[i, j] = 0
                    check += 1
    if check > 0:
        return True
    else:
        return False


def up():
    global score
    first_check = 0
    second_check = 0

    if shift_up():
        first_check += 1

    for i in range(Size):
        for j in range(Size - 1):
            if arr[j, i] == arr[j + 1, i] and arr[j, i] != 0 and arr[j + 1, i] != 0:
                second_check += 1
                arr[j, i] += arr[j + 1, i]
                score += arr[j, i]
                arr[j + 1, i] = 0
                shift_up()

    if first_check > 0 or second_check > 0:
        generate()


def down():
    global score
    first_check = 0
    second_check = 0

    if shift_down():
        first_check += 1

    for i in range(Size):
        for j in reversed(range(1, Size)):
            if arr[j, i] == arr[j - 1, i] and arr[j, i] != 0 and arr[j - 1, i] != 0:
                second_check += 1
                arr[j, i] += arr[j - 1, i]
                score += arr[j, i]
                arr[j - 1, i] = 0
                shift_down()

    if first_check > 0 or second_check > 0:
        generate()


def left():
    global score
    first_check = 0
    second_check = 0

    if shift_left():
        first_check += 1

    for i in range(Size):
        for j in range(Size - 1):
            if arr[i, j] == arr[i, j + 1] and arr[i, j] != 0 and arr[i, j + 1] != 0:
                second_check += 1
                arr[i, j] += arr[i, j + 1]
                score += arr[i, j]
                arr[i, j + 1] = 0
                shift_left()

    if first_check > 0 or second_check > 0:
        generate()


def right():
    global score
    first_check = 0
    second_check = 0

    if shift_right():
        first_check += 1

    for i in range(Size):
        for j in reversed(range(1, Size)):
            if arr[i, j] == arr[i, j - 1] and arr[i, j] != 0 and arr[i, j - 1] != 0:
                second_check += 1
                arr[i, j] += arr[i, j - 1]
                score += arr[i, j]
                arr[i, j - 1] = 0
                shift_right()

    if first_check > 0 or second_check > 0:
        generate()


def lose():
    rt = 0
    kt = 0

    for i in range(Size):
        for j in range(Size - 1):
            if arr[i, j] != arr[i, j + 1] and arr[i, j] != 0 and arr[i, j + 1] != 0:
                rt += 1

            if arr[j, i] != arr[j + 1, i] and arr[j, i] != 0 and arr[j + 1, i] != 0:
                kt += 1

    if rt == Size * (Size - 1) and kt == (Size - 1) * Size:
        return True
    else:
        return False


def win():
    for i in arr:
        if 2048 in i:
            return True
    else:
        return False
