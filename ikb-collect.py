#!/usr/bin/python3

# by Paul Opitz
# 2017-04-29
# Scrapes IKB Website and Weather API to collect visitor data of Innsbrucks' pools

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import json


page = requests.get("http://sas.ikb.at/ks/baeder_auslastung.aspx?segment=privat")
soup = BeautifulSoup(page.content, 'lxml')

try:
    #Amras
    amras = soup.find(id="cphInhalt_pnlHBA_Bad").find(class_="info-block").span.span.text
except AttributeError:
    amras = 100
try:
    #O-Dorf
     o_dorf = soup.find(id="cphInhalt_pnlHBO_Bad").find(class_="info-block").span.span.text
except AttributeError:
    o_dorf = 100
try:
    #Hötting
    hoetting = soup.find(id="cphInhalt_pnlHBH_Bad").find(class_="info-block").span.span.text
except AttributeError:
    hoetting = 100
    

# Current weather
OWMID = os.environ['OWMID']
weather_page = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Innsbruck,%20ATE&appid=' + OWMID)
weather = json.loads(weather_page.content)
temp = weather['main']['temp']
humidity = int(weather['main']['humidity'])/100
clouds = int(weather['clouds']['all'])/100

# Current time
timestamp = datetime.now()
year = timestamp.strftime('%Y')
month = timestamp.strftime('%m')
day = timestamp.strftime('%d')
hour = timestamp.strftime('%H')
minute = timestamp.strftime('%M')
day = timestamp.weekday()

row = [{'temp':temp, 'humidity':humidity,'year':year, 'clouds':clouds, 'timestamp':timestamp,'day':day, 'hour':hour, 'minute':minute, 'month':month, 'day':day,  'amras': int(amras)/100, 'o_dorf': int(o_dorf)/100, 'hoetting': int(hoetting)/100} ]
df = pd.DataFrame.from_dict(row)



# Write to CSV
if not os.path.isfile('ikb.csv'):
    df.to_csv('ikb.csv', header ='column_names', index=False)
else:
    df.to_csv('ikb.csv', mode = 'a', header=False, index=False)