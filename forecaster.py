import requests
import csv
from datetime import datetime, timedelta
import pprint
import pandas
import matplotlib.pyplot as plt
from sodapy import Socrata
import config

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

client = Socrata('data.cityofchicago.org', app_token = config.socratatoken, timeout = 3000)

#Google trend data
enddate = (datetime.now() - timedelta(days = 2)).strftime("%Y-%m-%d")
trendlink = f'https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222020-01-01%20{enddate}%22%2C%22resolution%22%3A%22WEEK%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22dma%22%3A%22602%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22covid%20symptoms%22%7D%5D%7D%7D%2C%7B%22geo%22%3A%7B%22dma%22%3A%22602%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22covid%20testing%20near%20me%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYHuhvzXTd_uuVJVhTL_xops6tpl6L3yc&tz=300'

download = requests.get(trendlink)
decoded_content = download.content.decode()
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
trend = list(cr)
#trend[>=3][0-2]

trend = getavg(trend, 4)
x = derivelist(trend, 0)
y = derivelist(trend, 1)

for i in range(len(y)):
    y[i] = y[i] * 10

# #City of Chicago traffic data
carlimit = 10000000
dailycars = client.get('kf7e-cur8', select = 'num_reads', order = 'time DESC', limit = carlimit)
dailytime = client.get('kf7e-cur8', select = 'time', order = 'time DESC', limit = carlimit)
dailycars = getvalues(dailycars)[::-1]
dailytime = getvalues(dailytime)[::-1]
dailycartime = dict(zip(dailytime, dailycars))
cardates, dailyaveragecars = dayavg(dailycartime)

#City of Chicago divvy bike data
bikelimit = 100000000
dailyavaildock = client.get('eq45-8inv', select = 'available_docks', order = 'timestamp DESC', limit = bikelimit)
dailybiketime = client.get('eq45-8inv', select = 'timestamp', order = 'timestamp DESC', limit = bikelimit)
dailyavaildock = getvalues(dailyavaildock)
dailybiketime = getvalues(dailybiketime)
dailyavailtime = dict(zip(dailybiketime,dailyavaildock))
bikedates, dailyaveragebikes = dayavg(dailyavailtime)

for i in range(len(dailyaveragebikes)):
    dailyaveragebikes[i] = dailyaveragebikes[i] * 10

plt.plot(cardates, dailyaveragecars)
plt.plot(x,y)
plt.plot(bikedates, dailyaveragebikes)
plt.show()

