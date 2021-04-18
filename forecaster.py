import requests
import csv
from datetime import datetime, timedelta
import pprint
import pandas
import matplotlib.pyplot as plt
from sodapy import Socrata
import config
import multiprocessing

def getavg(avglist, begin):
    output = []
    for i in range(begin, len(avglist)):
        for param in range(1, 3):
            if '<' in avglist[i][param]:
                avglist[i][param] = 0
        avg = (int(avglist[i][1])+int(avglist[i][2]))/2
        daylist = [avglist[i][0], avg]
        output.append(daylist)
    return output

def derivelist(derlist, select):
    output = []
    for param in derlist:
        output.append(param[select])
    return output

def getvalues(values):
    final = []
    keydict = list(values[0].keys())
    keydict = keydict[0]
    for i in values:
        try:
            final.append(int(i[keydict]))
        except Exception:
            try:
                final.append(i[keydict])
            except Exception:
                pass
    return final

def dayavg(datadict):
    dateoutput = []
    avgoutput = []
    counter = 0
    total = 0
    currenttime = ''
    for time, value in datadict.items():
        if time[:10] != currenttime:
            if currenttime != '':
                avg = total/counter
                avgoutput.append(avg)
                total = 0
                counter = 0
            currenttime = time[:10]
            dateoutput.append(currenttime)
        total += value
        counter += 1
    avg = total/counter
    avgoutput.append(avg)
    return dateoutput, avgoutput

def sevenMA(values, y, sevenday):
    if len(sevenday) != (len(values)-6):
        try:
            sevenday.append(sum(values[0+y:7+y])/7)
        except Exception:
            sevenday.append(0)
        y += 1
        return sevenMA(values, y, sevenday)
    else:
        return sevenday

client = Socrata('data.cityofchicago.org', app_token = config.socratatoken, timeout = 1000)

#Google trend data
enddate = (datetime.now() - timedelta(days = 2)).strftime("%Y-%m-%d")
trendlink = f'https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222020-01-01%202021-04-17%22%2C%22resolution%22%3A%22WEEK%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22dma%22%3A%22602%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22covid%20symptoms%22%7D%5D%7D%7D%2C%7B%22geo%22%3A%7B%22dma%22%3A%22602%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22covid%20testing%20near%20me%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYH0JAQunEQTcLO-tsuP6exb6steLIgej&tz=300'

download = requests.get(trendlink)
decoded_content = download.content.decode()
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
trend = list(cr)
#trend[>=3][0-2]

print('Google trend data recieved')

trend = getavg(trend, 4)
x = derivelist(trend, 0)
y = derivelist(trend, 1)
trend1 = dict(zip(x, y))

for i in range(len(y)):
    y[i] = y[i] * 10

print('Google trend data processed')

#City of Chicago traffic data
carlimit = 10000000
dailycars = client.get('kf7e-cur8', select = 'num_reads', where = 'time > "2020-01-01"', order = 'time DESC', limit = carlimit)
dailytime = client.get('kf7e-cur8', select = 'time', where = 'time > "2020-01-01"', order = 'time DESC', limit = carlimit)

print('City of Chicago traffic data recieved')

dailycars = getvalues(dailycars)[::-1]
dailytime = getvalues(dailytime)[::-1]
dailycartime = dict(zip(dailytime, dailycars))
cardates, dailyaveragecars = dayavg(dailycartime)
trend2 = dict(zip(cardates, dailyaveragecars))


print('City of Chicago traffic data processed')

#City of Chicago divvy bike data
bikelimit = 100000000
startdate = datetime(2020,1,1)
enddate = datetime(2021,4,17)
delta = timedelta(days=1)
dailyavaildock = []
dailybiketime = []
dailybiketime2 = []

while startdate <= enddate:
    dailyavaildock.extend(client.get('eq45-8inv',  select = 'available_docks', where = f'timestamp between "{startdate.strftime("%Y-%m-%d")}T12:00:00" and "{startdate.strftime("%Y-%m-%d")}T13:00:00"', order = 'timestamp DESC', limit = bikelimit))
    dailybiketime.extend(client.get('eq45-8inv', select = 'timestamp', where = f'timestamp between "{startdate.strftime("%Y-%m-%d")}T12:00:00" and "{startdate.strftime("%Y-%m-%d")}T13:00:00"', order = 'timestamp DESC', limit = bikelimit))
    dailyavaildock.extend(client.get('eq45-8inv',  select = 'available_docks', where = f'timestamp between "{startdate.strftime("%Y-%m-%d")}T17:00:00" and "{startdate.strftime("%Y-%m-%d")}T18:00:00"', order = 'timestamp DESC', limit = bikelimit))
    dailybiketime.extend(client.get('eq45-8inv', select = 'timestamp', where = f'timestamp between "{startdate.strftime("%Y-%m-%d")}T17:00:00" and "{startdate.strftime("%Y-%m-%d")}T18:00:00"', order = 'timestamp DESC', limit = bikelimit))
    print(startdate.strftime("%Y-%m-%d"))
    dailybiketime2.append(str(startdate.strftime("%Y-%m-%d")))
    startdate += delta

print('City of Chicago divvy bike data recieved')

dailyavaildock = getvalues(dailyavaildock)
dailybiketime = getvalues(dailybiketime)
dailyavailtime = dict(zip(dailybiketime,dailyavaildock))
bikedates, dailyaveragebikes = dayavg(dailyavailtime)
trend3 = dict(zip(dailybiketime2, dailyaveragebikes))

for i in range(len(dailyaveragebikes)):
    dailyaveragebikes[i] = dailyaveragebikes[i] * 20 

print('City of Chicago divvy bike data processed')

#Data manipulation
rows = []
fields = ['Date', 'GTrend', 'Traffic', 'Bike']

startdate = datetime(2020,1,1)
enddate = datetime(2021,4,18)
delta = timedelta(days=1)

while startdate <= enddate:
    temp = []
    temp.append(str(startdate.strftime("%Y-%m-%d")))
    try:
        temp.append(trend1[str(startdate.strftime("%Y-%m-%d"))])
    except Exception: 
        temp.append("")
    try:
        temp.append(trend2[str(startdate.strftime("%Y-%m-%d"))])
    except Exception: 
        temp.append("")
    try:
        temp.append(trend3[str(startdate.strftime("%Y-%m-%d"))])
    except Exception: 
        temp.append("")
    rows.append(temp)
    startdate += delta

with open('GFG', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(rows)

plt.plot(cardates, dailyaveragecars)
plt.plot(x,y)
plt.plot(dailybiketime2, dailyaveragebikes)
plt.show()