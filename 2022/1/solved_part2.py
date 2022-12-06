def get_top_three(list):
    list.sort()
    return list[1:]

f = open("./input.txt", "r")
maxVal = 0
maxVals = [0, 0, 0]
currentVal = 0
for x in f:
    if x == "\n":
        maxVal = max(currentVal, maxVal)
        maxVals.append(currentVal)
        maxVals = get_top_three(maxVals)
        print(maxVals)
        currentVal = 0
    else:
        currentVal = currentVal + int(x)

f.close()
print(sum(maxVals))

