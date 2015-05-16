#!/usr/bin/env python

import re
import sys
import urllib.request
from time import sleep, strftime
from PyQt4 import QtGui, QtCore
from bs4 import BeautifulSoup

__author__ = 'ozanenginoglu'

class Weather:

    def __init__(self):
        '''
        Containers are used to store all the information. Information is
        retrieved from the web site and then appended into various variables.
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
                print('Sleeping 1 second')
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
        '''
        Retrieve the current event link and its file name.
        '''
        link = self.soup.find('td', {'rowspan': '2'})
        re_search = re.findall(r'\/FILES.*png', str(link))
        re_url = 'http://www.mgm.gov.tr' + str(re_search[0])
        re_fileName = re.findall(r'-?..?\.png', str(link))
        self.eventURL.append(re_url)
        self.eventURL.append(re_fileName[0])

    def get_image(self):
        '''
        Retrieve the image from the server.
        '''
        image = urllib.request.urlretrieve(self.eventURL[0],
                                           'pictures/' + self.eventURL[1])
        image = QtGui.QPixmap('pictures/' + self.eventURL[1]).scaled(72, 72)
        return image

    def get_ALL(self, city='cigli'):
        '''
        Get all the information at once with this function.
        '''
        self.get_source(city)
        self.get_cityInfo()
        self.get_currentWeather()
        self.get_minTemperature()
        self.get_maxTemperature()
        self.get_minHumidity()
        self.get_maxHumidity()
        self.get_events()
        self.get_windSpeed()
        self.get_eventURL()

    def clean_containers(self):
        '''
        Remove all container lists.
        '''
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

    def __init__(self):

        super(WeatherGui, self).__init__()

        # Set QTimer for automatic update.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(60000)  # 1 minute
        self.timer.start()
        self.timer.timeout.connect(self.updateWeather)

        self.mgm = Weather()
        self.mgm.get_ALL()
        self.initUI()
        self.updateWeather()  # Update window at the beginning manually.

    def initUI(self):

        # Window Properties
        # self.setWindowFlags(QtCore.Qt.SplashScreen)
        self.setWindowTitle('MGM Havadurumu Uygulaması')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        # self.setFixedSize(350, 200)
        self.move(30, 600)

        # Layouts
        mainGrid = QtGui.QGridLayout()
        grid_currentWeather = QtGui.QGridLayout()
        grid_cityInfo = QtGui.QGridLayout()
        
        # Event Image
        self.currentEventPicture = QtGui.QLabel(self)

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

        self.label_currentTemp = QtGui.QLabel('')
        self.label_currentHumidity = QtGui.QLabel('')
        self.label_currentWind = QtGui.QLabel('')
        self.label_currentPressure = QtGui.QLabel('')
        self.label_currentSight = QtGui.QLabel('')

        grid_currentWeather.addWidget(self.label_currentTemp, 0, 2)
        grid_currentWeather.addWidget(self.label_currentHumidity, 1, 2)
        grid_currentWeather.addWidget(self.label_currentWind, 2, 2)
        grid_currentWeather.addWidget(self.label_currentPressure, 3, 2)
        grid_currentWeather.addWidget(self.label_currentSight, 4, 2)

        # City Info
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Gün Doğumu</b>'), 0, 0)
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Gün Batımı</b>'), 1, 0)
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Enlem</b>'), 2, 0)
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Boylam</b>'), 3, 0)
        grid_cityInfo.addWidget(QtGui.QLabel('<b>Yükseklik</b>'), 4, 0)
        grid_cityInfo.addWidget(verticalLine2, 0, 1, 5, 1)

        self.label_citySunrise = QtGui.QLabel('')
        self.label_citySunset = QtGui.QLabel('')
        self.label_cityLatitude = QtGui.QLabel('')
        self.label_cityLongtitude = QtGui.QLabel('')
        self.label_cityHeight = QtGui.QLabel('')

        grid_cityInfo.addWidget(self.label_citySunrise, 0, 2)
        grid_cityInfo.addWidget(self.label_citySunset, 1, 2)
        grid_cityInfo.addWidget(self.label_cityLatitude, 2, 2)
        grid_cityInfo.addWidget(self.label_cityLongtitude, 3, 2)
        grid_cityInfo.addWidget(self.label_cityHeight, 4, 2)

        # GroupBox
        groupBox_currentWeather = QtGui.QGroupBox('Günlük Havadurumu')
        groupBox_currentWeather.setLayout(grid_currentWeather)
        groupBox_cityInfo = QtGui.QGroupBox('Şehir Bilgileri')
        groupBox_cityInfo.setLayout(grid_cityInfo)

        # Buttons
        button_update = QtGui.QPushButton('Güncelle')
        button_update.clicked.connect(self.updateWeather)
        
        # Main Grid
        mainGrid.addWidget(self.currentEventPicture, 0, 0)
        mainGrid.addWidget(groupBox_currentWeather, 0, 2)
        mainGrid.addWidget(groupBox_cityInfo, 0, 1)
        # mainGrid.addWidget(button_update, 1, 2)

        self.setLayout(mainGrid)

    def updateWeather(self):

        old_currentWeather = self.mgm.currentWeather[0]
        self.mgm.clean_containers()
        self.mgm.get_ALL()
        if self.mgm.currentWeather[0] != old_currentWeather:
            print(self.mgm.currentWeather, strftime('%H:%M:%S'))

        # Set Image
        image = self.mgm.get_image()
        self.currentEventPicture.setFixedWidth(image.width())  # Set width
        self.currentEventPicture.setFixedHeight(image.height())  # Set height
        self.currentEventPicture.setPixmap(image)
        self.currentEventPicture.setToolTip(self.mgm.currentWeather[5])

        # Current Weather
        self.label_currentTemp.setText(self.mgm.currentWeather[0])
        self.label_currentHumidity.setText(self.mgm.currentWeather[1])
        self.label_currentWind.setText(self.mgm.currentWeather[2])
        self.label_currentPressure.setText(self.mgm.currentWeather[3])
        self.label_currentSight.setText(self.mgm.currentWeather[4])

        # City Info
        self.label_cityHeight.setText(self.mgm.cityInfo[0])
        self.label_cityLongtitude.setText(self.mgm.cityInfo[1])
        self.label_cityLatitude.setText(self.mgm.cityInfo[2])
        self.label_citySunset.setText(self.mgm.cityInfo[3])
        self.label_citySunrise.setText(self.mgm.cityInfo[4])


def main():
    application = QtGui.QApplication(sys.argv)
    window = WeatherGui()
    window.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
