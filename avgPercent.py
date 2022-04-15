from os import system
from math import gcd
import subprocess
import re

def takeMirror(pieces):
    mirror = ""
    piecesMirror = {
        "L": "J",
        "J": "L",
        "S": "Z",
        "Z": "S"
    }
    for c in pieces:
        if c in piecesMirror:
            mirror += piecesMirror[c]
        else:
            mirror += c
    return mirror

def removeChars(queue, build):
    build = list(build)
    queue = list(queue)
    for p in reversed(queue):
        if p in build:
            build.remove(p)
            queue.remove(p)
    return "".join(queue)

def matchSfinderInput(queue, pieces):
    # if pieces is empty always True
    if not pieces:
        return True
    
    pieces = pieces.split(",")
    BAG = "TILJSZO"
    for part in pieces:
        if part[0] in BAG:
            if queue[:len(part)] != part:
                return False
            else:
                queue = queue[len(part):]
        else:
            bag = []
            if part[0] == "*":
                bag = list(BAG)
            elif part[0] == "[":
                newRegex = re.search("\[(.*)\]", part).group(0)
                bag = re.findall(newRegex, BAG)
            else:
                raise "Pieces is incorrect"
            
            numPieces = len(bag)
            if part[-1].isnumeric():
                if len(bag) < int(part[-1]):
                    numPieces = int(part[-1])

            for i in range(numPieces):
                if queue[i] in bag:
                    bag.remove(queue[i])
                else:
                    return False
            queue = queue[numPieces:]
    
    return True

mirror = input("Mirror (y/n): ") == "y"
gluedAlready = input("Glued (y/n): ") == "y"
fractions = input("Fractions (y/n): ") == "y"
inputPieces = input("Pieces for setups: ")

glueFumen = "glueFumen.js"
fumenMirror = "fumenMirror.js"
fumenGetPieces = "fumenGetPieces.js"

avgPercent = 0

setups = open("setups.csv", "r")

# get values from the setups file
fumens = []
pieces = []
percents = []
for line in setups:
    data = line.rstrip().split("	")
    if len(data) == 3:
        fumen, percent, piece = data
    else:
        fumen, percent = data
        piece = ""
    fumens.append(fumen)
    pieces.append(piece)
    if fractions:
        percent = percent.rstrip().split("/")
        percent = int(percent[0]) / int(percent[1])
    else:
        percent = float(percent[:-1])/100
    percents.append(percent)
    if mirror:
        pieces.append(takeMirror(piece))
        percents.append(percent)
        

if mirror:
    fumenP = subprocess.Popen(["node", fumenMirror] + fumens, stdout=subprocess.PIPE)
    mirroredFumens = fumenP.stdout.read().decode().rstrip().split("\n")
    tmp = [None]*(len(fumens) * 2)
    tmp[::2] = fumens
    tmp[1::2] = mirroredFumens
    fumens = tmp

buildP = subprocess.Popen(["node", fumenGetPieces] + fumens, stdout=subprocess.PIPE)
builds = buildP.stdout.read().decode().rstrip().split("\n")

if gluedAlready:
    gluedFumens = fumens[:]
else:
    glueFumenP = subprocess.Popen(["node", glueFumen] + fumens, stdout=subprocess.PIPE)
    gluedFumens = glueFumenP.stdout.read().decode().rstrip().split("\n")
    if gluedFumens[-1][:7] == "Warning":
        print("\n".join(gluedFumens))
        exit()

osInput = f"java -jar sfinder.jar cover -t '{gluedFumens}' -p '{inputPieces}' -d 180"

system(osInput)

with open("output/cover.csv", "r") as outfile:
    lines = list(map(lambda x: x.rstrip().split(","), outfile.readlines()[1:]))

numQueues = len(lines)

percentOut = open("percentOut.txt", "w")
lastOut = open("lastOut.txt", "w")
# get the new highest
while percents:
    coverCount = 0
    highestPercent = max(percents)
    highestPercentIndex = percents.index(highestPercent)
    # read from bottom up and removes it and add to cover if covers
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        queue = ""
        if line[highestPercentIndex + 1] == "O":
            leftover = removeChars(line[0], builds[highestPercentIndex])
            # put the corresponding setup with percent in output file
            if matchSfinderInput(leftover, pieces[highestPercentIndex]):
                queue = lines.pop(i)[0]
                percentOut.write(queue + f'\t{highestPercent*100:.2f}%\t{fumens[highestPercentIndex]}\n')
                coverCount += 1
        
        # remove this setup from list
        if not queue:
            line.pop(highestPercentIndex + 1)
    
    # not covered at all
    print(f'{builds[highestPercentIndex]}: {fumens[highestPercentIndex]} {coverCount}')
    avgPercent += percents[highestPercentIndex] * (coverCount / numQueues)
    
    builds.pop(highestPercentIndex)
    pieces.pop(highestPercentIndex)
    percents.pop(highestPercentIndex)
    fumens.pop(highestPercentIndex)

num = round(avgPercent*25401600)
dem = 25401600
gcf = gcd(num, dem)
num = num // gcf
dem = dem // gcf
print(f'Average Percent: {avgPercent*100:.5f}% [{num}/{dem}]')
print("Queues not covered:\n" + "\n".join(map("".join, lines)))
percentOut.close()
