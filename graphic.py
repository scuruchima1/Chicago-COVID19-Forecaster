import os
import dateutil
import matplotlib
import pandas as pd
import config
from sodapy import Socrata
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.font_manager import FontProperties
from datetime import date, timedelta, datetime, time
from babel.dates import format_date, format_datetime, format_time

# Declarations 
client = Socrata("data.cityofchicago.org", config.socratatoken)

yesterday = str(date.today() - timedelta(days = 3)) + 'T00:00:00.000'
dt = datetime.fromisoformat(yesterday)
yesterdayword = format_date(dt, "MMMM dd, yyyy", locale='en_US')

# Useful functions
def combine(key,value):
    final = []
    for i in range(len(value)):
        temp = []
        if key[i] and value[i] != None:
            temp.append(key[i])
            temp.append(value[i])
            final.append(temp)
    return final

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

def dividevalues(dividend,divisor):
    return [round((i/j)*100,2) for i,j in zip(dividend,divisor)]

def trendcolor(trend):
    if trend[-1] < trend[-2]:
        return 'green'
    elif trend[-1 ] > trend[-2]:
        return 'red'
    elif trend[-1] == trend[-2]:
        return 'gray'

def trendindication(trend):
    if round(trend[-1],2) > round(trend[-2],2):
        return ('\n(▲ ' + str(round(round(trend[-1],2)-round(trend[-2],2),2)) + ')')
    elif round(trend[-1],2) < round(trend[-2],2):
        return ('\n(▼ ' + str(round(round(trend[-1],2)-round(trend[-2],2),2)) + ')')
    elif round(trend[-1],2) == round(trend[-2],2):
        return ('\n(| ' + str(round(round(trend[-1],2)-round(trend[-2],2),2)) + ')')

# 1st data set
# Daily Deaths & Cases
dailydeaths = client.get("naz8-j4nc",where = f"lab_report_date='{yesterday}'")[0]['deaths_total']
#dailycases = client.get("naz8-j4nc",where = f"lab_report_date='{yesterday}'")[0]['cases_total']
# Over Time Deaths & Cases
otdeaths = client.get("naz8-j4nc", select = 'deaths_total', order = 'lab_report_date')
#otcases = client.get("naz8-j4nc", select = 'cases_total')
otdate1 = client.get("naz8-j4nc", select = 'lab_report_date', order = 'lab_report_date')

# 2nd data set
# Daily Tests & Positive Tests
dailytests = client.get("gkdw-2tgv", where = f'date = "{yesterday}"')[0]['total_tests']
dailypositivetests = client.get("gkdw-2tgv", where = f'date = "{yesterday}"')[0]['positive_tests']
# Over Time Tests & Positive Tests 
ottests = client.get("gkdw-2tgv", select = 'total_tests', order='date')
otptests = client.get("gkdw-2tgv", select = 'positive_tests', order = 'date')
otdate2 = client.get("gkdw-2tgv", select = 'date', order='date')

# 3rd data set
# 3 day prediction with 11 real days
predictionurl = 'https://raw.githubusercontent.com/scuruchima1/Chicago-COVID19-Forecaster/main/data/prediction.csv'
prediction = pd.read_csv(predictionurl,names=['cases'])
prediction = prediction.values.tolist()
begindays = prediction[:-3]
predictiondays = prediction[-4:]

# Tweet text
dailyd = 'Deaths: ' + dailydeaths 
dailytp = "Tests: " + dailytests + "\nPostive Tests: " + dailypositivetests
positiverate = str(round((int(dailypositivetests)/int(dailytests))*100,2)) + '%'
tweetupdate = 'Updates for ' + yesterdayword +'\n'+ dailytp +'\n'+ dailyd + '\n' + "Positivity Rate: " + positiverate + '\n#Chicago #COVID19 #Statistics'

# Variables for 7-day stats
# Delta day finds difference in days to query the correct data in corresponding data sets
deltaday1 = (dateutil.parser.parse(getvalues(otdate1)[-1]) - dateutil.parser.parse(yesterday)).days
deltaday2 = (dateutil.parser.parse(getvalues(otdate2)[-1]) - dateutil.parser.parse(yesterday)).days
# 7-day moving averages before the delta days
sevendaynewcase = sevenMA(getvalues(otptests),0,[])
sevendaynewcase = sevendaynewcase[:-deltaday1]
sevendaypositivetest = sevenMA(dividevalues(getvalues(otptests),getvalues(ottests)),0,[])
sevendaypositivetest = sevendaypositivetest[:-deltaday2]
sevendaydeath = sevenMA(getvalues(otdeaths),0,[])
sevendaydeath = sevendaydeath[:-deltaday1]
sevendaytest = sevenMA(getvalues(ottests),0,[])
sevendaytest = sevendaytest[:-deltaday2]
# Trend line colors
sdnccolor = trendcolor(sevendaynewcase)
sdptcolor = trendcolor(sevendaypositivetest)
# Trend text 
sdncyesterday = trendindication(sevendaynewcase)
sdptyesterday = trendindication(sevendaypositivetest)
sddyesterday = trendindication(sevendaydeath)
sdtyesterday = trendindication(sevendaytest)

# Infographics
fig = plt.figure(constrained_layout=True,dpi=400)
fig.patch.set_facecolor('xkcd:azure')
fig.suptitle('Chicago COVID-19 (7-day average)', fontsize=14, fontweight='bold')
gs = fig.add_gridspec(4, 3)

# Text
xdistance = 0.69
plt.gcf().text(xdistance, 0.900, yesterdayword, fontsize=11, fontweight='bold') #0.85
plt.gcf().text(xdistance, 0.775, "New cases: \n" + str(round(sevendaynewcase[-1],2)) + sdncyesterday, fontsize=11) #0.70
plt.gcf().text(xdistance, 0.650, "Positivity rate: \n" + str(round(sevendaypositivetest[-1],2)) + '%' + sdptyesterday, fontsize=11) #0.55
plt.gcf().text(xdistance, 0.525, "New deaths: \n" + str(round(sevendaydeath[-1],2)) + sddyesterday, fontsize=11) #0.40
plt.gcf().text(xdistance, 0.400, "Tests conducted: \n" + str(round(sevendaytest[-1],2)) + sdtyesterday, fontsize=11) #0.25
plt.gcf().text(xdistance, 0.330, '@chicovid19', fontsize=11, fontweight='bold') #0.125

# 3 day case predictions
ax3 = fig.add_subplot(gs[3,-1])
ax3.plot([1,2,3,4,5,6,7,8,9,10,11],begindays)
ax3.plot([11,12,13,14],predictiondays,linestyle='dashed')
ax3.set_xlabel('3 Day case prediction', fontweight='bold')

# 7-day New case
ax1 = fig.add_subplot(gs[0:2,:-1])
ax1.plot(sevendaynewcase,color=sdnccolor)
plt.setp(ax1.get_xticklabels(), visible=False)
ax1.set_ylabel('New cases',fontweight='bold')

# 7-day Positivity rate 
ax2 = fig.add_subplot(gs[2:4,:-1])
ax2.plot(sevendaypositivetest,color=sdptcolor)
ax2.set_ylabel('Postivity rate %',fontweight='bold')
ax2.set_xlabel('Days since start of pandemic',fontweight='bold')

# Save figure as image
plt.savefig('cc.jpeg')
# Delete image
# os.remove('cc.jpeg')