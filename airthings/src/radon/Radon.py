# -*- coding: utf-8 -*-

import math
import time
import urllib2
import logging
import json
from base import Application, Plugin, ConfigurationString, configuration
from telldus import DeviceManager, Sensor


class RadonSensor(Sensor):
	def __init__(self, sensorId, serial):
		super(RadonSensor,self).__init__()
		self.sensorId = sensorId
                self.serial = serial
		self.setName('Radon 24h')

	def localId(self):
		return self.sensorId

        def model(self):
		return self.serial

	def typeString(self):
		return 'radon'
                
@configuration(
	serverAddress = ConfigurationString(
		defaultValue='192.168.1.164:8888',
		title='Server',
		description='Server Address and Port',
		minLength=1,
		maxLength=512
	)
)

class Radon(Plugin):
	def __init__(self):
		self.deviceManager = DeviceManager(self.context)
		self.sensor = None
            	Application().registerScheduledTask(self.updateValues, minutes=5, runAtOnce=True)

	def updateValues(self):
                host_url = 'http://' + self.config('serverAddress')
                try:
                        content = urllib2.urlopen(host_url).read()
                except Exception as e:
			logging.error('Could not request Wave value %s', e)
			return
                x = json.loads(content)
                for idx in x:
                        macStr = ""
                        for key in x[idx]:
                                #logging.info('idx %s', idx)
                                #logging.info('    key %s', key)
                                #logging.info('       val %s', x[idx][key])
                                if  key == 'Temperature':
                                        temperature = round(float(x[idx][key]),1)
                                elif key == 'Humidity':
                                    humidity = round(float(x[idx][key]))
                                elif key == 'Radon 24h avg':
                                        radon24h = round(float(x[idx][key]))
                                elif key == 'MAC':
                                        macStr = str(x[idx][key])
                                
                        if macStr:
                                idNum = 0x000000FFFFFF & int(macStr.translate(None, ":"), 16)
                                logging.info('Radon 24h is %f', radon24h)
                                logging.info('Humidity is %f', humidity)
                                logging.info('Temperature is %f', temperature)
                                logging.info('MAC Adddress is %s', macStr)
                                logging.info('SN is %s', idx)
                                logging.info('id Num is %d', idNum)

                	        self.sensor = RadonSensor(idNum, 'S/N:' + str(idx))
                                self.sensor.setSensorValue(Sensor.WATT, radon24h, Sensor.SCALE_POWER_WATT)
                                self.sensor.setSensorValue(Sensor.TEMPERATURE, temperature, Sensor.SCALE_TEMPERATURE_CELCIUS)
                                self.sensor.setSensorValue(Sensor.HUMIDITY, humidity, Sensor.SCALE_HUMIDITY_PERCENT)
			        self.deviceManager.addDevice(self.sensor)
			        self.deviceManager.finishedLoading('radon')
                        else:
                                logging.info('Error: server did not provide response. Make sure your device is in range and that the server has the correct MAC address.')
                
