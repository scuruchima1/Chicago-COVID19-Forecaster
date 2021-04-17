import requests
import csv
from datetime import datetime, timedelta
import pprint
import matplotlib.pyplot as plt

enddate = (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")
trendlink = f'https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222020-01-01%20{enddate}%22%2C%22resolution%22%3A%22WEEK%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%22dma%22%3A%22602%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22covid%20symptoms%22%7D%5D%7D%7D%2C%7B%22geo%22%3A%7B%22dma%22%3A%22602%22%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22covid%20testing%20near%20me%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYHuhvzXTd_uuVJVhTL_xops6tpl6L3yc&tz=300'

download = requests.get(trendlink)
decoded_content = download.content.decode()
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
trend = list(cr)
#trend[>=3][0-2]

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
        
trend = getavg(trend, 4)
x = derivelist(trend, 0)
y = derivelist(trend, 1)

plt.plot(x,y)
plt.show()