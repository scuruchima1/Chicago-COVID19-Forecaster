import csv
import numpy as np

# Datasets made:
# nobikeshifted3
# shifted3
# avgnobikeshifted3
# avgshifted3
# avg

def malist(array,index,ma):
    malist = []
    for val in range(1, len(array)):
        malist.append(float(array[val][index]))
    begin = len(malist)
    malist = np.array(malist)
    malist = np.convolve(malist, np.ones(ma), 'valid') / ma
    malist = malist.tolist()
    end = len(malist)
    print('items removed: ' + str(begin-end))
    return malist

dataset = csv.reader(open(r'data/trend.csv'))
dataset = list(dataset)
dataset = list(filter(([]).__ne__, dataset))

nobikeshifted = dataset.copy()
shifted = dataset.copy()
avgnobikeshifted = dataset.copy()
avgshifted = dataset.copy()
avg = dataset.copy()

delta = 3
 
# nobikeshifted dataset
for val in range(1,len(nobikeshifted)-delta):
    temp1 = nobikeshifted[-(val+delta)][2]
    temp2 = nobikeshifted[-(val+delta)][3]
    nobikeshifted[-val][2] = temp1
    nobikeshifted[-val][3] = temp2
nobikeshifted = np.array(nobikeshifted)
nobikeshifted = np.delete(nobikeshifted, 4, axis=1)
for row in range(1,delta+1):
    nobikeshifted = np.delete(nobikeshifted, 1, axis=0)
nobikeshifted = nobikeshifted.tolist()

writer = csv.writer(open(r'data/nobikeshifted3.csv', 'w'))
writer.writerows(nobikeshifted)

# shifted 
for val in range(1, len(nobikeshifted)-delta):
    temp1 = shifted[-(val+delta)][2]
    temp2 = shifted[-(val+delta)][3]
    temp3 = shifted[-(val+delta)][4]
    shifted[-val][2] = temp1
    shifted[-val][3] = temp2
    shifted[-val][3] = temp3
shifted = np.array(shifted)
for row in range(1,delta+1):
    shifted = np.delete(shifted, 1, axis=0)
shifted = shifted.tolist()

writer = csv.writer(open(r'data/shifted3.csv', 'w'))
writer.writerows(shifted)

#avgnobikeshifted
for val in range(1,len(avgnobikeshifted)-delta):
    temp1 = avgnobikeshifted[-(val+delta)][2]
    temp2 = avgnobikeshifted[-(val+delta)][3]
    avgnobikeshifted[-val][2] = temp1
    avgnobikeshifted[-val][3] = temp2
avgnobikeshifted = np.array(avgnobikeshifted)
avgnobikeshifted = np.delete(avgnobikeshifted, 4, axis=1)
for row in range(1,delta+1):
    avgnobikeshifted = np.delete(avgnobikeshifted, 1, axis=0)
avgnobikeshifted = avgnobikeshifted.tolist()
casesma = malist(avgnobikeshifted, 1, 7)
gtrendma = malist(avgnobikeshifted, 2, 7)
trafficma = malist(avgnobikeshifted, 3, 7)
casesma = np.array(casesma)
gtrendma = np.array(gtrendma)
trafficma = np.array(trafficma)
casesma = np.around(casesma, 2)
gtrendma = np.around(gtrendma, 2)
trafficma = np.around(trafficma, 2)
casesma = list(casesma)
gtrendma = list(gtrendma)
trafficma = list(trafficma)
del avgnobikeshifted[1:7]
for row in range(1,len(avgnobikeshifted)):
    avgnobikeshifted[row][1] = casesma[row-1]
    avgnobikeshifted[row][2] = gtrendma[row-1]
    avgnobikeshifted[row][3] = trafficma[row-1]

writer = csv.writer(open(r'data/avgnobikeshifted3.csv', 'w'))
writer.writerows(avgnobikeshifted)

#avgshifted 
for val in range(1,len(avgshifted)-delta):
    temp1 = avgshifted[-(val+delta)][2]
    temp2 = avgshifted[-(val+delta)][3] 
    temp3 = avgshifted[-(val+delta)][4]
    avgshifted[-val][2] = temp1
    avgshifted[-val][3] = temp2
    avgshifted[-val][4] = temp3
avgshifted = np.array(avgshifted)
for row in range(1,delta+1):
    avgshifted = np.delete(avgshifted, 1, axis=0)
avgshifted = avgshifted.tolist()
casesma = np.array(malist(avgshifted, 1, 7))
gtrendma = np.array(malist(avgshifted, 2, 7))
trafficma = np.array(malist(avgshifted, 3, 7))
bikema = np.array(malist(avgshifted, 4, 7))
casesma = np.around(casesma, 2)
gtrendma = np.around(gtrendma, 2)
trafficma = np.around(trafficma, 2)
bikema = np.around(bikema, 2)
casesma = list(casesma)
gtrendma = list(gtrendma)
trafficma = list(trafficma)
bikema = list(bikema)
del avgshifted[1:7]
for row in range(1,len(avgshifted)):
    avgshifted[row][1] = casesma[row-1]
    avgshifted[row][2] = gtrendma[row-1]
    avgshifted[row][3] = trafficma[row-1]
    avgshifted[row][4] = bikema[row-1]

writer = csv.writer(open(r'data/avgshifted3.csv', 'w'))
writer.writerows(avgshifted)

#avg 
casesma = list(np.around(np.array(malist(avg, 1, 7)), 2))
gtrendma = list(np.around(np.array(malist(avg, 2, 7)), 2))
trafficma = list(np.around(np.array(malist(avg, 3, 7)), 2))
bikema = list(np.around(np.array(malist(avg, 4, 7)), 2))
del avg[1:7]
for row in range(1,len(avg)):
    avg[row][1] = casesma[row-1]
    avg[row][2] = gtrendma[row-1]
    avg[row][3] = trafficma[row-1]    
    avg[row][4] = bikema[row-1]

writer = csv.writer(open(r'data/avg.csv', 'w'))
writer.writerows(avg)
