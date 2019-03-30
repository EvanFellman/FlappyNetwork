import os
import random
import time
import decimal
os.system('mode con: cols=174 lines=48')

pipesFlownThrough = 0

playerHeight = 17
playerVelocity = 1

pipeWidth = 10
pipeHeight = 10
numPipes = 2
pipes = []
fitness = 0

layerValues = [[]]

def sigma(x):
    if x < 0:
        return 0
    return x


class Neuron:
    def __init__(self, strRep=""):
        x = strRep.split(":")
        self.bias = float(x[0])
        self.weights = x[1::]
        for i in range(len(self.weights)):
            self.weights[i] = float(self.weights[i])
    def calc(self, inputs):
        sum = self.bias
        for i in range(len(inputs)):
            sum += inputs[i] * self.weights[i]
        return sigma(sum)

    def mutate(self):
        for i in range(len(self.weights)):
            self.weights[i] += ((random.random() / 20) - 0.025) + self.weights[i]

    def child(self, other):
        for i in range(len(self.weights)):
            self.weights[i] = (self.weights[i] + other.weights[i]) / 2

    def toString(self):
        stri = str(self.bias)
        for i in self.weights:
            stri += ":" + str(i)
        return stri


class Network:
    def __init__(self, strRep):
        self.layers = []
        x = strRep.split("|")[1::]
        for i in range(len(x)):
            self.layers.append([])
            for j in range(len(x[i].split(",")))[1::]:
                self.layers[i].append(Neuron(x[i].split(",")[j]))
    def toString(self):
        str = ""
        for j in self.layers:
            str += "|"
            for i in j:
                str += ","
                str += i.toString()
        return str

    def calc(self, inputs):
        global layerValues
        layerValues = [inputs]
        for i in range(len(self.layers)):
            layerValues.append([])
            for j in range(len(self.layers[i])):
                layerValues[i + 1].append(self.layers[i][j].calc(layerValues[i]))
        return layerValues[len(layerValues) - 1]

f = open("BestFlappyNetwork.txt","r")
net = Network(f.read().split("\n")[1])
f.close

def display():
    global layerValues
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
    for i in layerValues:
        string += "\n"
        for x in i:
            string += "{:.5E}".format(float(str(x))) + "\t"
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
    if net.calc([playerHeight, closestPipeHeight()[1], closestPipeHeight()[0] / 8])[0] > 0:
        playerVelocity = -0.3
    else:
        playerVelocity = 0.3
    time.sleep(0.005)
    fitness += 1
