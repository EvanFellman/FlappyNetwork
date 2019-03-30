import os
import random
import time
import decimal
import keyboard

os.system('mode con: cols=174 lines=48')

pipesFlownThrough = 0

playerHeight = 17
playerVelocity = 1

pipeWidth = 10
pipeHeight = 10
numPipes = 1
pipes = []
fitness = 0


def display():
    string = " |"
    out = True
    if playerHeight < 0 or playerHeight > 35:
        return True
    for i in range(36):
        for j in range(150):
            flag = True
            for y in pipes:
                if flag and j == 2 and i == round(playerHeight):
                    string += "v"
                    out = flag and j <= y[1] + (pipeWidth / 2) and j >= y[1] - (pipeWidth / 2) \
                          and (i > y[0] + (pipeHeight / 2) or i < y[0] - (pipeHeight / 2))
                    flag = False
                if flag and j <= y[1] + (pipeWidth / 2) and j >= y[1] - (pipeWidth / 2) \
                        and (i > y[0] + (pipeHeight / 2) or i < y[0] - (pipeHeight / 2)):
                    string += "."
                    flag = False
                    if j == 2 and i == round(playerHeight):
                        out = True
            if flag:
                string += " "
        string += "|\n |"
    string = string[:-2:] + ("=" * 154) + "\n"
    print("\033[H\033[J" + ("=" * 154) + "\n" + string + "\n\npipes flown through: " + str(pipesFlownThrough) + "\n")
    return out


def closestPipeHeight():
    minX = 9999
    y = 10000
    for i in pipes:
        if i[1] < minX:
            y = i[0]
            minX = i[1]
    return (minX, y)


while True:
    if display():
        playerHeight = 10
        playerVelocity = 1
        pipes = []
        pipesFlownThrough = 0
        for i in range(numPipes):
            pipes += [[random.randint(pipeHeight, 35 - pipeHeight), (i + 1) * (150 / numPipes)]]
        fitness = 0
    for y in pipes:
        y[1] -= 1
        if y[1] < -0.5 * pipeWidth:
            y[0] = random.randint(round(pipeHeight / 2), round(35 - (pipeHeight / 2)))
            y[1] = 149 + (pipeWidth / 2)
            pipesFlownThrough += 1
    playerHeight += playerVelocity
    if keyboard.KEY_DOWN and keyboard.is_pressed(' '):
        playerVelocity = -0.3
    else:
        playerVelocity = 0.3
    time.sleep(0.0025)
    fitness += 1


















