#!/usr/bin/env python

import re
import sys
import urllib.request
from time import sleep
from PyQt4 import QtGui, QtCore
from bs4 import BeautifulSoup

__author__ = 'ozanenginoglu'


class Weather:

    def __init__(self):
        '''
        Containers are used to store all the information. They are first
        retrieved from the web site and then appended into them in each
        function defined in Weather Class.
        '''
        self.cityInfo = []  # Height, longtitude,latitude, sunset and sunrise
        self.currentWeather = []  # Temp, RH, Wind, Pressure, Line Sight, Event
        self.minTemperature = []  # Minimum temperatures
        self.maxTemperature = []  # Maximum temperatures
        self.minHumidity = []  # Minimum humidities
        self.maxHumidity = []  # Maximum humidities
        self.events = []  # Events
        self.eventURL = []  # Event URLs
        self.windSpeed = []  # Wind speeds
        print('Weather information is being pulled from the web server...')

    def get_source(self, city):
        '''
        Retrieve weather data from mgm.gov.tr web site and transform it into
        a soup file which beautifulsoup can work on.
        '''
        # Base page URL
        url = 'http://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?m='
        url += str(city)  # City name
        while True:
            # Get the web page source code. If it fails wait 1 second
            # self.assertNotIn(member, container)d try again until it's done.
            try:
                # Load the web page and save it to the variable
                source_code = urllib.request.urlopen(url)
                break
            except:
                sleep(1)  # Wait 1 second
        self.soup = BeautifulSoup(source_code)  # source code to Beautifulsoup
        return self.soup

    def get_cityInfo(self):
        '''
        Current weather information of the city.
        '''
        for i in self.soup.findAll('div', {'id': 'divMerkez'}):
            text = i.text.split()  # Split the whole text into parts
            city_height = text[1] + ' ' + text[2]
            city_longtitude = text[4] + text[5] + ' ' + text[6]
            city_latitude = text[8] + text[9] + ' ' + text[10]
            city_sunset = text[13]
            city_sunrise = text[16]
            self.cityInfo.append(city_height)
            self.cityInfo.append(city_longtitude)
            self.cityInfo.append(city_latitude)
            self.cityInfo.append(city_sunset)
            self.cityInfo.append(city_sunrise)

    def get_currentWeather(self):
        '''
        Retrieves today's weather conditions such as temperature, humidity,
        pressure, wind speed and line of sight.
        '''
        for i in self.soup.findAll('td'):
            for j in i.findAll('em'):
                self.currentWeather.append(j.text)
        for i in self.soup.findAll('table', {'class': 'tbl_sond'}):
            for j in i.findAll('td', {'rowspan': '2'}):
                self.currentWeather.append(j['title'])

    def get_minTemperature(self):
        '''
        Minimum temperature data of the following
        five days.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmMin'
                                              + str(i)}):
                self.minTemperature.append(j.text)

    def get_maxTemperature(self):
        '''
        Maximum temperature data of the following five days.
        '''

        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmMax'
                                              + str(i)}):
                self.maxTemperature.append(j.text)

    def get_minHumidity(self):
        '''
        Minimum humidity data of the following five days.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmNemMin'
                                              + str(i)}):
                self.minHumidity.append(j.text)

    def get_maxHumidity(self):
        '''
        Maximum humidity data of the following five days.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmNemMax'
                                              + str(i)}):
                self.maxHumidity.append(j.text)

    def get_events(self):
        '''
        Weather events of the following five days. Such as cloudy, sunny etc.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('img', {'id': 'cp_sayfa_imgHadise'
                                               + str(i)}):
                self.events.append(j['alt'])

    def get_windSpeed(self):
        '''
        Wind speed of the following five days.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmRuzgarHiz'
                                              + str(i)}):
                self.windSpeed.append(j.text)

    def get_eventURL(self):
        # Retrieve the current event link and its file name.
        link = self.soup.find('td', {'rowspan': '2'})
        re_search = re.findall(r'\/FILES.*png', str(link))
        re_url = 'http://www.mgm.gov.tr' + str(re_search[0])
        re_fileName = re.findall(r'-?..?\.png', str(link))
        self.eventURL.append(re_url)
        self.eventURL.append(re_fileName[0])

    def clean_containers(self):
        # Remove all the appended list items.
        self.cityInfo[:] = []
        self.currentWeather[:] = []
        self.minTemperature[:] = []
        self.maxTemperature[:] = []
        self.minHumidity[:] = []
        self.maxHumidity[:] = []
        self.events[:] = []
        self.eventURL[:] = []
        self.windSpeed[:] = []
        

class WeatherGui(QtGui.QWidget, Weather):

    def loadPage(self):
            self.mgm.get_source('izmir')
            self.mgm.get_cityInfo()
            self.mgm.get_currentWeather()
            self.mgm.get_minTemperature()
            self.mgm.get_maxTemperature()
            self.mgm.get_minHumidity()
            self.mgm.get_maxHumidity()
            self.mgm.get_events()
            self.mgm.get_windSpeed()
            self.mgm.get_eventURL()

    def __init__(self):
        super(WeatherGui, self).__init__()
        self.mgm = Weather()
        self.initUI()

    def initUI(self):
        self.loadPage()
        # Window Properties
        # self.setWindowFlags(QtCore.Qt.SplashScreen)
        self.setWindowTitle('MGM Havadurumu Uygulaması')
        # self.setFixedSize(350, 200)
        self.move(30, 600)

        # Event Image
        image = urllib.request.urlretrieve(self.mgm.eventURL[0],
                                           self.mgm.eventURL[1])
        image = QtGui.QPixmap(self.mgm.eventURL[1]).scaled(72, 72)
        self.currentEventPicture = QtGui.QLabel(self)
        self.currentEventPicture.setFixedWidth(image.width())  # Set width
        self.currentEventPicture.setFixedHeight(image.height())  # Set height
        self.currentEventPicture.setPixmap(image)  # Link the image file
        self.currentEventPicture.setToolTip(self.mgm.currentWeather[5])

        mainGrid = QtGui.QGridLayout()
        grid_currentWeather = QtGui.QGridLayout()
        grid_cityInfo = QtGui.QGridLayout()

        # Vertical Lines
        verticalLine1 = QtGui.QFrame()
        verticalLine1.setFrameStyle(QtGui.QFrame.VLine)
        verticalLine1.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                    QtGui.QSizePolicy.Expanding)
        verticalLine2 = QtGui.QFrame()
        verticalLine2.setFrameStyle(QtGui.QFrame.VLine)
        verticalLine2.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                    QtGui.QSizePolicy.Expanding)

        # Current Weather GroupBox Items
        grid_currentWeather.addWidget(QtGui.QLabel('<b>Sıcaklık</b>'), 0, 0)
        grid_currentWeather.addWidget(QtGui.QLabel('<b>Nem</b>'), 1, 0)
        grid_currentWeather.addWidget(QtGui.QLabel('<b>Rüzgar</b>'), 2, 0)
        grid_currentWeather.addWidget(QtGui.QLabel('<b>Basınç</b>'), 3, 0)
        grid_currentWeather.addWidget(QtGui.QLabel('<b>Görüş</b>'), 4, 0)
        grid_currentWeather.addWidget(verticalLine1, 0, 1, 5, 1)
        grid_currentWeather.addWidget(QtGui.QLabel
                                      (self.mgm.currentWeather[0]), 0, 2)
        grid_currentWeather.addWidget(QtGui.QLabel
                                      (self.mgm.currentWeather[1]), 1, 2)
        grid_currentWeather.addWidget(QtGui.QLabel
                                      (self.mgm.currentWeather[2]), 2, 2)
        grid_currentWeather.addWidget(QtGui.QLabel
                                      (self.mgm.currentWeather[3]), 3, 2)
        grid_currentWeather.addWidget(QtGui.QLabel
                                      (self.mgm.currentWeather[4]), 4, 2)

        # City Info
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Gün Doğumu</b>'), 0, 0)
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Gün Batımı</b>'), 1, 0)
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Enlem</b>'), 2, 0)
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Boylam</b>'), 3, 0)
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Yükseklik</b>'), 4, 0)
        grid_cityInfo.addWidget(verticalLine2, 0, 1, 5, 1)
        grid_cityInfo.addWidget(QtGui.QLabel(self.mgm.cityInfo[4]), 0, 2)
        grid_cityInfo.addWidget(QtGui.QLabel(self.mgm.cityInfo[3]), 1, 2)
        grid_cityInfo.addWidget(QtGui.QLabel(self.mgm.cityInfo[2]), 2, 2)
        grid_cityInfo.addWidget(QtGui.QLabel(self.mgm.cityInfo[1]), 3, 2)
        grid_cityInfo.addWidget(QtGui.QLabel(self.mgm.cityInfo[0]), 4, 2)

        # GroupBox
        groupBox_currentWeather = QtGui.QGroupBox('Günlük Havadurumu')
        groupBox_currentWeather.setLayout(grid_currentWeather)
        groupBox_cityInfo = QtGui.QGroupBox('Şehir Bilgileri')
        groupBox_cityInfo.setLayout(grid_cityInfo)

        # Buttons
        button_update = QtGui.QPushButton('Güncelle')
        button_update.clicked.connect(self.update)

        # Main Grid
        mainGrid.addWidget(self.currentEventPicture, 0, 0)
        mainGrid.addWidget(groupBox_currentWeather, 0, 2)
        mainGrid.addWidget(groupBox_cityInfo, 0, 1)
        # mainGrid.addWidget(button_update, 1, 2)

        self.setLayout(mainGrid)


def main():
    application = QtGui.QApplication(sys.argv)
    window = WeatherGui()
    window.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
