# Chicago-COVID19-Forecaster
Chicago COVID-19 Forecaster is a forecaster program that takes data from google search trends, Chicago street congestion data, and divvy bike data to formulate a forecast on the spread of COVID-19 in Chicago. 

# Python Scripts 
- datagather.py, Gathers data from multiple APIs and puts them in the master data set, trend.csv
- forecaster.py, Machine learning script that makes a model to forecast new cases for the next 3 days. This script makes a 14-day data set with 11 real days and 3 predicted days in, prediction.csv
- graphic.py, Makes a graphic to show the 3 predicted case days along with positivity rate and new case graphs. This graphic is used for the @ChiCovid19 twitter.
- makesets.py, Makes many different data sets to train our machine learning model and to predict new cases for the next 3 days. 
- visualizedata.py, Visualizes the 7-day moving average of the raw data (this data set is avg.csv).

# Data CSVs
- trend.csv, raw data values in with columns (date, cases, gtrend, traffic, bike)
  *date, YYYY-MM-DD
  *cases, confirmed cases
  gtrend, google trend average score for "covid symptoms" and "covid testing near me" in Chicago
  traffic, average GPS pings in different Chicago regions
  bike, average bikes being used per dock in Chicago
- avg.csv, all raw data values put into a 7-day moving average, first 6 raw days are removed.
- prediction.csv, 14-day data set with 11 real days and 3 predicted days
- Next data sets are usually used to train the machine learning model
- shifted3.csv, all columns except for date and cases shifted down 3 days
- avgshifted3.csv, all columns except for date and cases shifted down 3 days, columns are then set to a 7-day moving average
- nobikeshifted3.csv, bike column removed, all columns except for date and cases shifted down 3 days
- avgnobikeshifted3.csv, bike column removed, all columns except for date and cases shifted down 3 days, columns are then set to a 7-day moving average

