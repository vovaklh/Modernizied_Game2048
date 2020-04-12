from tkinter import *
from random import randrange
from tkinter.messagebox import *
from threading import Thread
from multiprocessing import Pool


class _2048operate:
    def __init__(self, block, score=0):
        self.block = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        copyBlock(self.block, block)
        self.score = score

    def getNewBlock(self):
        i = randrange(0, 4)
        j = randrange(0, 4)
        p = randrange(0, 10)
        while self.block[i][j] != 0:
            i = randrange(0, 4)
            j = randrange(0, 4)
        if p == 0:
            self.block[i][j] = 4
        else:
            self.block[i][j] = 2

    def judgeOver(self):
        flagFill = 1
        flagCombine = 0
        for i in range(4):
            for j in range(4):
                if self.block[i][j] == 0:
                    flagFill = 0
        if flagFill == 1:
            for i in range(4):
                for j in range(4):
                    if (j < 3 and self.block[i][j] == self.block[i][j + 1]) or (
                            i < 3 and self.block[i][j] == self.block[i + 1][j]):
                        flagCombine = 1
        if flagFill == 1 and flagCombine == 0:
            return 0
        else:
            return 1

    def operate(self, turn):
        flagMove = self.combine(turn)
        if flagMove >= 1:
            self.getNewBlock()
        return flagMove

    def blockRotate(self, turn):
        temp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        if turn == 'along':
            for i in range(4):
                for j in range(4):
                    temp[i][j] = self.block[3 - j][i]
        elif turn == 'inverse':
            for i in range(4):
                for j in range(4):
                    temp[i][j] = self.block[j][3 - i]
        for i in range(4):
            for j in range(4):
                self.block[i][j] = temp[i][j]

    def combine(self, turn):  # 0:left,1:up,2:right,3:down
        if turn == 'up' or turn == 'Up' or turn == 1:
            self.blockRotate('inverse')
        elif turn == 'right' or turn == 'Right' or turn == 2:
            self.blockRotate('along')
            self.blockRotate('along')
        elif turn == 'down' or turn == 'Down' or turn == 3:
            self.blockRotate('along')
        flag = 1
        flagMove = 0
        while flag == 1:
            flag = 0
            for i in range(4):
                for j in range(3):
                    if self.block[i][j + 1] != 0 and self.block[i][j] == 0:
                        flag = 1
                        flagMove = 1
                        k = j
                        while k < 3:
                            self.block[i][k] = self.block[i][k + 1]
                            k = k + 1
                        self.block[i][3] = 0
        for i in range(4):
            for j in range(3):
                if self.block[i][j] != 0 and self.block[i][j] == self.block[i][j + 1]:
                    self.block[i][j] *= 2
                    self.block[i][j + 1] = 0
                    self.score += self.block[i][j]
                    k = j + 1
                    flagMove += self.block[i][j]
                    while k < 3:
                        self.block[i][k] = self.block[i][k + 1]
                        k = k + 1
                    self.block[i][3] = 0
        if turn == 'up' or turn == 'Up' or turn == 1:
            self.blockRotate('along')
        elif turn == 'right' or turn == 'Right' or turn == 2:
            self.blockRotate('inverse')
            self.blockRotate('inverse')
        elif turn == 'down' or turn == 'Down' or turn == 3:
            self.blockRotate('inverse')
        return flagMove


def copyBlock(myblock, block):
    for i in range(4):
        for j in range(4):
            myblock[i][j] = block[i][j]


def maxA(arr, length, layer):
    list = []
    for j in range(layer):
        max = -100000000
        num = -1
        for i in range(length):
            if arr[i] >= max and not i in list:
                max = arr[i]
                num = i
        list.append(num)
    return list


def log2(num):
    i = 1
    while num > 2:
        num /= 2
        i += 1
    return i


class AI2048:
    def __init__(self, block):
        self.perlife = [0] * 10
        self.block = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        copyBlock(self.block, block)

    def assess1(self, turn, k, m, n, l):
        tempgame = _2048operate(self.block)
        if tempgame.combine(turn) == 0:
            assess = -10000000
        else:
            assess = k * self.numSpace() + m * self.smooth() + n * self.continuity() + 10 * tempgame.score
        return assess

    def numSpace(self):
        space = 0
        for i in range(4):
            for j in range(4):
                if self.block[i][j] == 0:
                    space += 1
        return space

    def continuity(self):
        conScore = 0
        for i in range(4):
            for j in range(4):
                if j < 3 and self.block[i][j] > self.block[i][j + 1]:
                    conScore += 10 * i * (3 - j)
                else:
                    conScore -= 10 * i * (3 - j)
                if i > 0 and self.block[i][j] > self.block[i - 1][j]:
                    conScore += 10
                else:
                    conScore -= 10
        return conScore

    def smooth(self):
        smoothScore = 0
        for i in range(4):
            for j in range(4):
                if self.block[i][j] == 0:
                    continue
                else:
                    if i > 0 and self.block[i - 1][j] != 0:
                        smoothScore -= (log2(self.block[i][j]) - log2(self.block[i - 1][j])) ** 2
                    if i < 3 and self.block[i + 1][j] != 0:
                        smoothScore -= (log2(self.block[i][j]) - log2(self.block[i + 1][j])) ** 2
                    if j > 0 and self.block[i][j - 1] != 0:
                        smoothScore -= (log2(self.block[i][j]) - log2(self.block[i][j - 1])) ** 2
                    if j < 3 and self.block[i][j + 1] != 0:
                        smoothScore -= (log2(self.block[i][j]) - log2(self.block[i][j + 1])) ** 2
        return smoothScore

    def assess(self, k, m, n, l):
        assess = [0, 0, 0, 0]
        for turn in range(4):
            assess[turn] = self.assess1(turn, k, m, n, l)
        return maxA(assess, 4, 1)[0]

    def tryMove(self):
        perlife = [0, 0, 0, 0]
        avi = []
        for turn in range(4):
            if self.assess1(turn, 100, 5, 5, 10) > -1000000:
                avi.append(turn)
        for turn in avi:
            for i in range(30):
                mygame = _2048operate(self.block, 0)
                life = 0
                mygame.operate(turn)
                while (mygame.judgeOver() == 1):
                    d = randrange(0, 4)
                    flagMove = mygame.operate(d)
                    if flagMove >= 1:
                        life += 1
                perlife[turn] += life
        return maxA(perlife, 4, 1)[0]

    def threadTry(self, turn, j):
        life = [0] * 100
        self.perlife[j] = 0
        for i in range(30):
            mygame = _2048operate(self.block, 0)
            life[i] = 0
            mygame.operate(turn)
            while (mygame.judgeOver() == 1):
                d = randrange(0, 4)
                mygame.operate(d)
                life[i] += 1
            self.perlife[j] += life[i]
        self.perlife[j] /= 3
