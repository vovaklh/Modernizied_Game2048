import pygame
import Logic_2048
import os
from tkinter import *
from tkinter import messagebox
import speech_recognition as sr
import threading
import cv2
import numpy as np
import keyboard
from AI_Bot_2048 import _2048operate, AI2048
import time

# Start to record video
cap = cv2.VideoCapture(0)
hand_cascade = cv2.CascadeClassifier('hand.xml')

# Append coordinates to list
list_of_xy = []


# Detect direction of movement and make a move
def cv_make_move():
    variance_of_x = np.var(np.array([i[0] for i in list_of_xy]))
    variance_of_y = np.var(np.array([i[1] for i in list_of_xy]))
    if variance_of_x > variance_of_y:
        if list_of_xy[0][0] - list_of_xy[len(list_of_xy) - 1][0] > 0:
            Logic_2048.right()
            show()
        else:
            Logic_2048.left()
            show()
    else:
        if list_of_xy[0][1] - list_of_xy[len(list_of_xy) - 1][1] > 0:
            Logic_2048.up()
            show()
        else:
            Logic_2048.down()
            show()
    list_of_xy.clear()

# Create csv file with human game
def make_csv(x, y):
    X_array.append(x)
    Y_array.append(y)
    if len(X_array) > 70:
        stacked_array = np.column_stack((X_array, Y_array))
        np.savetxt("human_game.csv", stacked_array, delimiter=',')

# Detect hand on video
def computer_vision():
    count = 0
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hands = hand_cascade.detectMultiScale(gray, 1.5, 2)
        contour = hands
        contour = np.array(contour)

        if count > 0:

            if len(contour) == 1:
                cv2.putText(img=frame, text='Movement', org=(int(100 / 2 - 20), int(100 / 2)),
                            fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1,
                            color=(0, 255, 0))
                for (x, y, w, h) in hands:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    list_of_xy.append([x, y])

            elif len(contour) == 0:
                cv2.putText(img=frame, text='Static', org=(int(100 / 2 - 20), int(100 / 2)),
                            fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1,
                            color=(0, 0, 255))

        count += 1

        if len(list_of_xy) == 33:
            cv_make_move()

        cv2.imshow('Movement_tracking', frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# Function that recognize a speech
def speech_recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="ru-RU").lower()
    except sr.UnknownValueError:
        text = speech_recognition()
    return text


# Speech function make move
def change_array(text):
    if 'вверх' in text:
        Logic_2048.up()
        show()
    elif 'вниз' in text:
        Logic_2048.down()
        show()
    elif 'права' in text:
        Logic_2048.right()
        show()
    elif 'лево' in text:
        Logic_2048.left()
        show()


# Recognize a text and define the move
def get_command():
    while True:
        change_array(speech_recognition())


# Monte-Carlo method to solve 2048 game
def ai():
    my_game = _2048operate(list(Logic_2048.arr), Logic_2048.score)
    while (my_game.judgeOver() == 1):
        if (Logic_2048.win() or Logic_2048.lose()):
            break
        if keyboard.is_pressed('q'):
            break
        my_game = _2048operate(list(Logic_2048.arr), Logic_2048.score)
        ai2048 = AI2048(list(Logic_2048.arr))
        if ai2048.numSpace() > 4:
            turn = ai2048.assess(100, 5, 5, 10)
        else:
            turn = ai2048.tryMove()
        my_game.operate(turn)
        Logic_2048.arr = np.array(my_game.block)
        Logic_2048.score = my_game.score
        show()
        time.sleep(0.15)


def get_colour(i):
    return color_dict[i]


white = (255, 255, 255)
gray = (130, 130, 130)
black = (0, 0, 0)

color_dict = {
    0: (130, 130, 130),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

blocks = 4
size_block = 110
margin = 10
width = blocks * size_block + (blocks + 1) * margin
height = width + 110
title_rec = pygame.Rect(0, 0, width, 110)

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

my_font = pygame.font.SysFont('Verdana.ttf', 50)
score_font = pygame.font.SysFont('Verdana.ttf', 50)

X_array = []
Y_array = []


def show():
    pygame.draw.rect(screen, white, title_rec)
    for row in range(blocks):
        for col in range(blocks):
            w = col * size_block + (col + 1) * margin
            h = row * size_block + (row + 1) * margin + 110
            pygame.draw.rect(screen, get_colour(Logic_2048.arr[row, col]), (w, h, 110, 110))

            array = my_font.render(str(Logic_2048.arr[row, col]), 1, (0, 0, 0))

            if Logic_2048.arr[row, col] != 0:
                place = array.get_rect(center=(w + (size_block / 2), h + (size_block / 2)))
                screen.blit(array, place)
    score_value = score_font.render('Score:' + str(Logic_2048.score), 1, (0, 0, 0))
    screen.blit(score_value, (10, 30))
    pygame.display.update()


def main():
    Logic_2048.new_game()
    show()
    while True:
        if Logic_2048.lose():
            Logic_2048.new_game()
            window = Tk()
            window.wm_withdraw()
            messagebox.showinfo("Окончание игры", "К сожалению, вы проиграли")
            window.destroy()
            window.quit()
        elif Logic_2048.win():
            Logic_2048.new_game()
            window = Tk()
            window.wm_withdraw()
            messagebox.showinfo("Победа", "Поздравляем, Вы выиграли")
            window.destroy()
            window.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Logic_2048.up()
                    make_csv(Logic_2048.arr.flatten(), 1)
                if event.key == pygame.K_DOWN:
                    Logic_2048.down()
                    make_csv(Logic_2048.arr.flatten(), 2)
                if event.key == pygame.K_LEFT:
                    Logic_2048.left()
                    make_csv(Logic_2048.arr.flatten(), 3)
                if event.key == pygame.K_RIGHT:
                    Logic_2048.right()
                    make_csv(Logic_2048.arr.flatten(), 4)
                if event.key == pygame.K_c:
                    t_cv.start()
                if event.key == pygame.K_s:
                    t_speech.start()
                if event.key == pygame.K_a:
                    ai()

        clock.tick(50)
        show()


t_speech = threading.Thread(target=get_command)
t_speech.daemon = True

t_cv = threading.Thread(target=computer_vision)
t_cv.daemon = True

main()
