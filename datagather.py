import requests
import csv
from datetime import datetime, timedelta
import pprint
import pandas
from sodapy import Socrata
import config
from pytrends.dailydata import get_daily_data

#Useful functions 
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

def getvalues(values, startval = 0):
    final = []
    keydict = list(values[startval].keys())
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
                avg = round(avg, 2)
                avgoutput.append(avg)
                total = 0
                counter = 0
            currenttime = time[:10]
            dateoutput.append(currenttime)
        total += value
        counter += 1
    avg = total/counter
    avg = round(avg, 2)
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

def shortdate(dates):
    for i in range(len(dates)):
        dates[i] = dates[i][:10]

def fillempty(dataset,field):
    counter = 0
    for row in range(len(dataset)):
        if dataset[row][field] == '':
            counter += 1 
        if dataset[row][field] != '':
            if counter != 0:
                start = row - counter
                endvalue = float(dataset[row][field])
                try:
                    startvalue = float(dataset[start-1][field])
                except Exception:
                    startvalue = 0
                totalvalue = endvalue - startvalue
                increment = totalvalue/counter
                for fillin in range(1,counter+1):
                    endvalue -= increment
                    dataset[row-fillin][field] = round(endvalue,2)
                counter = 0

# Declarations
client = Socrata('data.cityofchicago.org', app_token = config.socratatoken, timeout = 1000)

gtrendrun = True
if gtrendrun == True:
    #Google trend data
    #Pytrend API calls for covid symptoms and covid testing near me

    print('Google trend data gathering')

    gtrend1 = get_daily_data('covid symptoms', start_year=2020, start_mon=3, stop_year=2021, stop_mon=4 , geo= 'US-IL-602')
    gtrend2 = get_daily_data('covid testing near me', start_year=2020, start_mon=3, stop_year=2021, stop_mon=4 , geo= 'US-IL-602')

    print('Google trend data recieved')

    #Convert pandas arrary to list
    listtrend1 = gtrend1.values.tolist()
    listtrend2 = gtrend2.values.tolist()
    #List declarations for trend values
    valuestrend1 = []
    valuestrend2 = []
    #List declarations for average trend values
    combinedavgtrend = []
    #List declaration for dates
    trenddates = []

    #Adding trend values to corresponding lists
    for lines in listtrend1:
        valuestrend1.append(round(lines[4],2))
    for lines in listtrend2:
        valuestrend2.append(round(lines[4],2))

    #Adding average trend values to corresponding list
    for value in range(len(valuestrend1)):
        avgval = round(((valuestrend1[value] + valuestrend2[value]) / 2 ),2)
        combinedavgtrend.append(avgval)

    #Adding dates to corresponding list
    startdate = datetime(2020,3,1)
    delta = timedelta(days=1)
    for length in range(len(combinedavgtrend)):
        trenddates.append(startdate.strftime("%Y-%m-%d"))
        startdate += delta

    #Dictionary declaration for values and dates
    trend1 = dict(zip(trenddates, combinedavgtrend))

    print('Google trend data processed')

coctd = True
if coctd == True:
    #City of Chicago traffic data

    print('City of Chicago traffic data gathering')

    carlimit = 10000000
    dailycars = client.get('kf7e-cur8', select = 'num_reads', where = 'time > "2020-03-01"', order = 'time DESC', limit = carlimit)
    dailytime = client.get('kf7e-cur8', select = 'time', where = 'time > "2020-03-01"', order = 'time DESC', limit = carlimit)

    print('City of Chicago traffic data recieved')

    dailycars = getvalues(dailycars)[::-1]
    dailytime = getvalues(dailytime)[::-1]
    dailycartime = dict(zip(dailytime, dailycars))
    cardates, dailyaveragecars = dayavg(dailycartime)
    trend2 = dict(zip(cardates, dailyaveragecars))

    print('City of Chicago traffic data processed')

cocbd = True
if cocbd == True:
    #City of Chicago divvy bike data
    bikelimit = 100000000
    startdate = datetime(2020,3,1)
    #Make enddate always be current day
    enddate = datetime(2021,4,26)
    delta = timedelta(days=1)
    dailyavaildock = []
    dailybiketime = []
    dailybiketime2 = []

    print('City of Chicago divvy bike data gathering')

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

coccd = True
if coccd == True:
    #City of Chicago daily case data

    print('City of Chicago daily case data gathering')

    dailycases = client.get('naz8-j4nc', select = 'cases_total', order = 'lab_report_date DESC', limit = 3000 )
    dailycasesdates = client.get('naz8-j4nc', select = 'lab_report_date', order = 'lab_report_date DESC', limit = 3000 )

    print('City of Chicago daily case data recieved')
    #try lab_report_date ACSEN 
    dailycases = getvalues(dailycases)[::-1]
    dailycasesdates = getvalues(dailycasesdates, 1)[::-1]
    shortdate(dailycasesdates)
    #Check this line V
    dailycases.pop()
    trend4 = dict(zip(dailycasesdates, dailycases))

    print('City of Chicago daily case data processed')

datamanipulation = True
if datamanipulation == True:
    #Data manipulation
    rows = []
    fields = ['Date', 'Cases', 'GTrend', 'Traffic', 'Bike']

    startdate = datetime(2020,3,1)
    #Make enddate always be current day
    enddate = datetime(2021,4,26)
    delta = timedelta(days=1)

    #Master data set assembly 
    while startdate <= enddate:
        temp = []
        temp.append(str(startdate.strftime("%Y-%m-%d")))
        try:
            temp.append(trend4[str(startdate.strftime("%Y-%m-%d"))])
        except Exception: 
            temp.append("")
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

    with open(r'data/trend.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)

    try:
        dataset = csv.reader(open(r'data/trend.csv'))
        dataset = list(dataset)
        dataset = list(filter(([]).__ne__, dataset))
        fillempty(dataset, 2)
        fillempty(dataset, 3)
        writer = csv.writer(open(r'data/trend.csv', 'w'))
        writer.writerows(dataset)
    except Exception:
        print('Empty values not filled')

