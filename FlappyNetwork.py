import time
import random
import math
import os


showBefore = True
os.system('mode con: cols=174 lines=48')
skipTo = input("What generation should I skip to?\n")
if skipTo == '':
    skipTo = 0
else:
    showBefore = not "true" == (
        input("\n\nShould I hide the generations I am skipping? (answer True or False)\n")).lower()
    skipTo = int(skipTo)

try:
    f = open("BestFlappyNetwork.txt", "r")
    if f.read() == "":
        q = open("BestFlappyNetwork.txt", "w")
        q.write("0\n0")
        q.close()
    f.close()
except Exception:
    q = open("BestFlappyNetwork.txt", "w")
    q.write("0\n0")
    q.close()

if not showBefore:
    print("wait...\ngeneration: 1")
skipTo -= 2

generationSize = 100

playerHeight = 17
playerVelocity = 1

startSpeciesTime = time.time()

maxFitness = (0, 0, None)

pipeWidth = 10
pipeHeight = 10
numPipes = 1
pipes = []
for i in range(numPipes):
    pipes += [[random.randint(pipeHeight, 35 - pipeHeight), (i + 1) * (150 / numPipes)]]


def sigma(x):
    if x < 0:
        return 0
    return x
    # return x
    return 1 / (1 + pow(math.e, -1 * x))


class Neuron:
    def __init__(self, numInputs=-1, strRep=""):
        if numInputs != -1:
            self.weights = []
            for i in range(numInputs):
                self.weights += [(4 * random.random()) - 2]
            self.bias = (4 * random.random()) - 2
        else:
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
        out = Neuron(strRep=self.toString())
        for i in range(len(self.weights)):
            out.weights[i] += ((random.random() / 20) - 0.025) + self.weights[i]
        out.bias = ((random.random() / 20) - 0.025)
        return out
    def toString(self):
        stri = str(self.bias)
        for i in self.weights:
            stri += ":" + str(i)
        return stri


class Network:
    def __init__(self, layersSizes=[], strRep=""):
        if layersSizes != []:
            self.layers = [[]]
            for i in range(layersSizes[0]):
                x = Neuron(layersSizes[0])
                x.weights[0] = 1
                self.layers[0].append(x)
            for i in range(len(layersSizes))[1::]:
                self.layers.append([])
                for _ in range(layersSizes[i]):
                    self.layers[i].append(Neuron(layersSizes[i - 1]))
        else:
            self.layers = []
            x = strRep.split("|")[1::]
            for i in range(len(x)):
                x[i] = Neuron(x[i].split(",")[1::])

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

    def mutate(self):
        out = Network([1])
        out.layers = []
        for x in self.layers:
            wowieDuder = []
            for i in x:
                wowieDuder.append(i)
            out.layers.append(wowieDuder)
        for i in range(len(out.layers)):
            for j in range(len(out.layers[i])):
                out.layers[i][j] = out.layers[i][j].mutate()
        return out

# will display pipes and player by printing to console
# outputs True iff player is in a pipe
def display():
    string = " |"
    out = True
    if not (showBefore or generationNumber > skipTo):
        if playerHeight < 0 or playerHeight > 35:
            return True
        for i in pipes:
            if 2 <= i[1] + (pipeWidth / 2) and 2 >= i[1] - (pipeWidth / 2) \
                    and (playerHeight > i[0] + (pipeHeight / 2) or playerHeight < i[0] - (pipeHeight / 2)):
                return True
        return False
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
    print("\033[H\033[J" + ("=" * 154) + "\n" + string + "\n\n\nfitness: " + str(fitness) +
          "\ngeneration: " + str(generationNumber + 1) + "\t\t\tspecies: " + str(speciesNumber + 1) +
          "\t\t\tbest fitness so far: " + str(maxFitness[0]) + " (gen " + str(maxFitness[1]) + ")")
    return out


generation = []
for i in range(generationSize):
    generation += [Network([3, 5, 1])]

layerValues = []
generationNumber = 0
speciesNumber = 0
fitness = 0


def merge(list1, list2, acc=[]):
    if list1 == []:
        if list2 == []:
            return acc
        else:
            return acc + list2
    elif list2 == []:
        return acc + list1
    if list1[0][1] > list2[0][1]:
        return merge(list1[1::], list2, acc + [list1[0]])
    else:
        return merge(list2[1::], list1, acc + [list2[0]])


def mergeSort(list):
    if len(list) < 2:
        return list
    else:
        return merge(mergeSort(list[:len(list) // 2:]), mergeSort(list[len(list) // 2::]))


def sumFitness(list, acc=0):
    if list == []:
        return acc
    else:
        return sumFitness(list[1::], acc=list[0][1] + acc)


def closestPipeHeight():
    minX = 9999
    y = 10000
    for i in pipes:
        if i[1] < minX:
            y = i[0]
            minX = i[1]
    return (minX, y)


def save():
    t = open("BestFlappyNetwork.txt", "r")
    f = t
    t = t.read().split("\n")
    if int(t[0]) < fitness:
        q = open("BestFlappyNetwork.txt", "w")
        q.write(str(fitness) + "\n" + generation[speciesNumber].toString())
        q.close()
    f.close()


while True:
    if display():
        startSpeciesTime = time.time()
        # creature died
        if fitness >= maxFitness[0]:
            maxFitness = fitness, generationNumber + 1, generation[speciesNumber]
        save()

        # keep the network but also attach the fitness it got
        generation[speciesNumber] = [generation[speciesNumber], fitness]
        fitness = 0
        playerHeight = 10
        playerVelocity = 1

        pipes = []
        for i in range(numPipes):
            pipes += [[random.randint(pipeHeight, 35 - pipeHeight), (i + 1) * (150 / numPipes)]]

        if speciesNumber == len(generation) - 1:
            if not showBefore or generationNumber > skipTo:
                print("generation: " + str(generationNumber + 2))
            # that was the last one in its generation
            # kill bottom 3/4 and give the top 1/4 four children each??????
            # yea sounds good (enough) to me
            newGeneration = []
            generation = mergeSort(generation)

            for i in range((len(generation) // 4)):
                for _ in range(4):
                    newGeneration.append(generation[i][0].mutate())
            generation = newGeneration

            speciesNumber = 0
            generationNumber += 1
        else:
            speciesNumber += 1

    else:
        fitness += 1
        if fitness % 1000 == 0:
            save()
        if time.time() - startSpeciesTime > 0.05:
            skipTo = 1

    for y in pipes:
        y[1] -= 1
        if y[1] < -0.5 * pipeWidth:
            y[0] = random.randint(round(pipeHeight / 2), round(35 - (pipeHeight / 2)))
            y[1] = 149 + (pipeWidth / 2)
    playerHeight += playerVelocity
    if generation[speciesNumber].calc([playerHeight, closestPipeHeight()[1], closestPipeHeight()[0] / 8])[0] > 0:
        playerVelocity = -0.3
    else:
        # playerVelocity += gravity
        playerVelocity = 0.3
    if generationNumber > skipTo:
        time.sleep(0.015)
