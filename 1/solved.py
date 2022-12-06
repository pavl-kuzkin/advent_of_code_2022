f = open("./input.txt", "r")
maxVal = 0
currentVal = 0
for x in f:
    if x == "\n":
        maxVal = max(currentVal, maxVal)
        currentVal = 0
    else:
        currentVal = currentVal + int(x)




f.close()
print(maxVal)