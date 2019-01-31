# -*- coding: utf-8 -*-

import math
import time
import urllib2
import logging
from base import Application, Plugin, ConfigurationString, configuration
from telldus import DeviceManager, Sensor


class RadonSensor(Sensor):
	def __init__(self, sensorId):
		super(RadonSensor,self).__init__()
		self.sensorId = sensorId
		self.setName('Radon 24h')

	def localId(self):
		return self.sensorId

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
	        data = content.split(',')
                timeStamp  = data[0]
                if timeStamp:
                        temperature = round(float(data[1]),1)
                        humidity    = round(float(data[2]),1)
                        radon24h    = round(float(data[3]))
                        #radonLong  = float(data[4])
                        macStr      = data[5]              
                        idNum       = 0x000000FFFFFF & int(macStr.translate(None, ":"), 16)
                        logging.info('Radon 24h is %f', radon24h)
                        logging.info('Humidity is %f', humidity)
                        logging.info('Temperature is %f', temperature)
                        logging.info('MAC Adddress is %s', macStr)
                        logging.info('id Num is %d', idNum)

		        if self.sensor is None:
                	        self.sensor = RadonSensor(idNum)
                                self.sensor.setSensorValue(Sensor.WATT, radon24h, Sensor.SCALE_POWER_WATT)
                                self.sensor.setSensorValue(Sensor.TEMPERATURE, temperature, Sensor.SCALE_TEMPERATURE_CELCIUS)
                                self.sensor.setSensorValue(Sensor.HUMIDITY, humidity, Sensor.SCALE_HUMIDITY_PERCENT)
			        self.deviceManager.addDevice(self.sensor)
			        self.deviceManager.finishedLoading('radon')
		        else:
                                self.sensor.setSensorValue(Sensor.WATT, radon24h, Sensor.SCALE_POWER_WATT)
                                self.sensor.setSensorValue(Sensor.TEMPERATURE, temperature, Sensor.SCALE_TEMPERATURE_CELCIUS)
                                self.sensor.setSensorValue(Sensor.HUMIDITY, humidity, Sensor.SCALE_HUMIDITY_PERCENT)
                else:
                        logging.info('Error: server did not provide response. Make sure your device is in range and that the server has the correct MAC address.')
                
