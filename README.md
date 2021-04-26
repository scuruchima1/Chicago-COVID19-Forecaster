# Chicago COVID-19 Forecaster
Chicago COVID-19 Forecaster is a forecaster program that takes data from google search trends, Chicago street congestion data, and divvy bike data to formulate a forecast on the spread of COVID-19 in Chicago. 

[![forthebadge made-with-python](https://img.shields.io/badge/python-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ChiCovid19 Twitter](https://img.shields.io/badge/ChiCovid19-%231DA1F2.svg?&style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/chicovid19/)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?&style=for-the-badge)]()

## Python Scripts 
- datagather.py, Gathers data from multiple APIs and puts them in the master data set, trend.csv
- forecaster.py, Machine learning script that makes a model to forecast new cases for the next 3 days. This script makes a 14-day data set with 11 real days and 3 predicted days in, prediction.csv
- graphic.py, Makes a graphic to show the 3 predicted case days along with positivity rate and new case graphs. This graphic is used for the @ChiCovid19 twitter.
- makesets.py, Makes many different data sets to train our machine learning model and to predict new cases for the next 3 days. 
- visualizedata.py, Visualizes the 7-day moving average of the raw data (this data set is avg.csv).

## Data CSVs
1. trend.csv, raw data values in with columns (date, cases, gtrend, traffic, bike)
  - date, YYYY-MM-DD
  - cases, confirmed cases
  - gtrend, google trend average score for "covid symptoms" and "covid testing near me" in Chicago
  - traffic, average GPS pings in different Chicago regions
  - bike, average bikes being used per dock in Chicago
2. avg.csv, all raw data values put into a 7-day moving average, first 6 raw days are removed.
3. prediction.csv, 14-day data set with 11 real days and 3 predicted days
4. shifted3.csv, all columns except for date and cases shifted down 3 days
5. avgshifted3.csv, all columns except for date and cases shifted down 3 days, columns are then set to a 7-day moving average
6. nobikeshifted3.csv, bike column removed, all columns except for date and cases shifted down 3 days
7. avgnobikeshifted3.csv, bike column removed, all columns except for date and cases shifted down 3 days, columns are then set to a 7-day moving average

## Order Of Scripts
- Scripts should be run in the following order to ensure proper results
1. datagather.py
2. makesets.py
3. forecaster.py
- The following scripts have no proper order and serve as visual aids
1. graphic.py
2. visualizedata.py
