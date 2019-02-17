# -*- coding: utf-8 -*-

import math
import time
import urllib2
import logging
import json
from base import Application, Plugin, ConfigurationString, configuration
from telldus import DeviceManager, Sensor


class RadonSensor(Sensor):
	def __init__(self, sensorId):
		super(RadonSensor,self).__init__()
		self.sensorId = sensorId
		self.setName('Radon')

	def localId(self):
		return self.sensorId

        def model(self):
		return 'wave'

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
		self.sensors = {}
		#self.deviceManager.removeDevicesByType('radon')
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
                                if  key == 'Temperature':
                                        temperature = round(float(x[idx][key]),1)
                                elif key == 'Humidity':
                                        humidity = round(float(x[idx][key]))
                                elif key == 'Radon 24h avg':
                                        radon24h = round(float(x[idx][key]))
                                elif key == 'Radon long term':
                                        radonlong = round(float(x[idx][key]))
                                elif key == 'MAC':
                                        macStr = str(x[idx][key])
                                elif key == 'DateTime':
                                        datetime = str(x[idx][key])
                                else:
                                        logging.info('Unknown key: %s', key)
                                        
                        if macStr:
                                idNum = int(macStr.translate(None, ":"), 16)
                                logging.info('Radon 24h is %f', radon24h)
                                logging.info('Radon long is %f', radonlong)
                                logging.info('Humidity is %f', humidity)
                                logging.info('Temperature is %f', temperature)
                                logging.info('MAC Adddress is %s', macStr)
                                logging.info('DateTime is %s', datetime)
                                logging.info('SN is %s', idx)
                                logging.info('id Num is %d', idNum)

                                if idNum not in self.sensors:
                                        logging.info('Added new sendsor %d', idNum)
                	                self.sensors[idNum] = RadonSensor(idNum)
                                        self.sensors[idNum].setSensorValue(Sensor.WATT, radon24h, Sensor.SCALE_POWER_WATT)
                                        self.sensors[idNum].setSensorValue(Sensor.WATT, radonlong, Sensor.SCALE_POWER_KWH)
                                        self.sensors[idNum].setSensorValue(Sensor.TEMPERATURE, temperature, Sensor.SCALE_TEMPERATURE_CELCIUS)
                                        self.sensors[idNum].setSensorValue(Sensor.HUMIDITY, humidity, Sensor.SCALE_HUMIDITY_PERCENT)
                                        self.deviceManager.addDevice(self.sensors[idNum])
			                self.deviceManager.finishedLoading('radon')
		                else:
                                        logging.info('Updated sendsor %d', idNum)
                                        self.sensors[idNum].setSensorValue(Sensor.WATT, radon24h, Sensor.SCALE_POWER_WATT)
                                        self.sensors[idNum].setSensorValue(Sensor.WATT, radonlong, Sensor.SCALE_POWER_KWH)
                                        self.sensors[idNum].setSensorValue(Sensor.TEMPERATURE, temperature, Sensor.SCALE_TEMPERATURE_CELCIUS)
                                        self.sensors[idNum].setSensorValue(Sensor.HUMIDITY, humidity, Sensor.SCALE_HUMIDITY_PERCENT)
                        else:
                                logging.info('Error: server did not provide response. Make sure your device is in range and that the server has the correct MAC address.')
                
