#!/usr/bin/env python

__author__ = 'ozanenginoglu'

import urllib.request
from bs4 import BeautifulSoup
from time import sleep

class Weather:

    def __init__(self):
        '''
        Containers are used to store all the information.
        They are first retrieved from the web site and then
        appended into them in each function defined in Weather
        Class.
        '''
        self.city_info_container = [] # Height, longtitude, latitude, sunset and sunrise
        self.current_weather_container = [] # Temperature, Relative Humidity, Wind Speed, Pressure, Line Sight, Event
        self.min_temp_container = [] # Minimum temperatures
        self.max_temp_container = [] # Maximum temperatures
        self.min_humidity_container = [] # Minimum humidities
        self.max_humidity_container = [] # Maximum humidities
        self.events_container = [] # Events
        self.wind_speed_container = [] # Wind speeds
        print('Weather information is being pulled from the web server...')
        
    def get_weather(self, city):
        '''
        Retrieve weather data from mgm.gov.tr web site
        and transform it into a soup file which
        beautifulsoup can work on.
        '''
        url = 'http://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?m=' # Base page url
        url += str(city) # City name
        while True: # Get the web page source code. If it fails wait 1 second and try again until it's done.
            try:
                source_code = urllib.request.urlopen(url) # Load the web page and save it to the variable
                break
            except:
                sleep(1) # Wait 1 second
        self.soup = BeautifulSoup(source_code) # Turn source code into Beautifulsoup file.
        return self.soup

    def city_info(self):
        '''
        Current weather information of the city.
        '''
        for i in self.soup.findAll('div',{'id':'divMerkez'}):
            text = i.text.split() # Split the whole text into parts
            city_height = text[1] + ' ' + text[2]
            city_longtitude = text[4] + text[5] + ' ' + text[6]
            city_latitude = text[8] + text[9] + ' ' + text[10]
            city_sunset = text[13]
            city_sunrise = text[16]
            self.city_info_container.append(city_height)
            self.city_info_container.append(city_longtitude)
            self.city_info_container.append(city_latitude)
            self.city_info_container.append(city_sunset)
            self.city_info_container.append(city_sunrise)
    
    def current_weather(self):
        '''
        Retrieves today's weather conditions such as
        temperature, humidity, pressure, wind speed
        and line of sight.
        '''
        for i in self.soup.findAll('td'):
            for j in i.findAll('em'):
                self.current_weather_container.append(j.text)
        for i in self.soup.findAll('table', {'class':'tbl_sond'}):
            for j in i.findAll('td', {'rowspan':'2'}):
                self.current_weather_container.append(j['title'])

    def weather_temperature_minimums(self):
        '''
        Minimum temperature data of the following
        five days.
        '''
        for i in range(1,6):
            for j in self.soup.findAll('td',{'id':'cp_sayfa_thmMin' + str(i)}):
                self.min_temp_container.append(j.text)

    def weather_temperature_maximums(self):
        '''
        Maximum temperature data of the following
        five days.
        '''
        for i in range(1,6):
            for j in self.soup.findAll('td',{'id':'cp_sayfa_thmMax' + str(i)}):
                self.max_temp_container.append(j.text)

    def weather_humidity_minimums(self):
        '''
        Minimum humidity data of the following
        five days.
        '''
        for i in range(1,6):
            for j in self.soup.findAll('td',{'id':'cp_sayfa_thmNemMin' + str(i)}):
                self.min_humidity_container.append(j.text)

    def weather_humidity_maximums(self):
        '''
        Maximum humidity data of the following
        five days.
        '''
        for i in range(1,6):
            for j in self.soup.findAll('td',{'id':'cp_sayfa_thmNemMax' + str(i)}):
                self.max_humidity_container.append(j.text)

    def weather_events(self):
        '''
        Weather events of the following five
        days. Such as "cloudy, sunny etc."
        '''
        for i in range(1,6):
            for j in self.soup.findAll('img',{'id':'cp_sayfa_imgHadise' + str(i)}):
                self.events_container.append(j['alt'])

    def weather_wind(self):
        '''
        Wind speed of the following five days.
        '''
        for i in range(1,6):
            for j in self.soup.findAll('td',{'id':'cp_sayfa_thmRuzgarHiz' + str(i)}):
                self.wind_speed_container.append(j.text)

    def weather_output(self):
        '''
        Print out the containers
        '''
        ## container_names=['current_weather','current_humidity','current_wind','current_pressure','current_line_of_sight','current_event',
        ##                  'minTemp1','minTemp2','minTemp3','minTemp4','minTemp5',
        ##                  'maxTemp1','maxTemp2','maxTemp3','maxTemp4','maxTemp5',
        ##                  'minHumidity1','minHumidity2','minHumidity3','minHumidity4','minHumidity5',
        ##                  'maxHumidity1','maxHumidity2','maxHumidity3','maxHumidity4','maxHumidity5',
        ##                  'event1','event2','event3','event4','event5',
        ##                  'wind1','wind2','wind3','wind4','wind5']
        ## container_dictionary = dict(zip(container_names,self.container))
        ## print(container_dictionary['event1'])
        print('City Info', end = ' >> ')
        print(self.city_info_container)
        print('Current City Weather Info', end = ' >> ')
        print(self.current_weather_container)
        print('Minimum Temperatures', end = ' >> ')
        print(self.min_temp_container)
        print('Maximum Temperatures', end = ' >> ')
        print(self.max_temp_container)
        print('Minimum Humiditys', end = ' >> ')
        print(self.min_humidity_container)
        print('Maximum Humiditys', end = ' >> ')
        print(self.max_humidity_container)
        print('Events of the following five days', end = ' >> ')
        print(self.events_container)
        print('Wind Speeds', end = ' >> ')
        print(self.wind_speed_container)
    
mgm = Weather()
mgm.get_weather('IZMIR')
mgm.city_info()
mgm.current_weather()
mgm.weather_temperature_minimums()
mgm.weather_temperature_maximums()
mgm.weather_humidity_minimums()
mgm.weather_humidity_maximums()
mgm.weather_events()
mgm.weather_wind()

mgm.weather_output()
