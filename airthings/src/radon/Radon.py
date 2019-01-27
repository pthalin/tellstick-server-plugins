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
		minLength=4,
		maxLength=512
	)
)

class Radon(Plugin):
	def __init__(self):
		self.deviceManager = DeviceManager(self.context)
		self.sensor = None
            	Application().registerScheduledTask(self.updateValues, minutes=5, runAtOnce=True)

	def updateValues(self):
                #values = []
                host_url =  'http://' + self.config('serverAddress')
                content = urllib2.urlopen(host_url).read()
                data = content.split(',')
                #timeStamp   = float(data[0])
                temperature = float(data[1])
                humidity    = float(data[2])
                radon24h    = float(data[3])
                #radonLong   = float(data[4])

                logging.info('Radon 24h is %f', radon24h)
                logging.info('Humidity is %f', humidity)
                logging.info('Temperature is %f', temperature)

		if self.sensor is None:
                        #todo: use  id codecs.encode(device.mac, "hex_codec")
			self.sensor = RadonSensor(10)
                        self.sensor.setSensorValue(Sensor.WATT, radon24h, Sensor.SCALE_POWER_WATT)
			self.deviceManager.addDevice(self.sensor)
			self.deviceManager.finishedLoading('radon')
		else:
                        self.sensor.setSensorValue(Sensor.WATT, radon24h, Sensor.SCALE_POWER_WATT)


                #values.append({'type': Sensor.TEMPERATURE, 'value': temperature, 'scale': Sensor.SCALE_TEMPERATURE_CELCIUS})
                #values.append({'type': Sensor.HUMIDITY,    'value': humidity,    'scale': Sensor.SCALE_HUMIDITY_PERCENT})
                #values.append({'type': Sensor.UNKNOWN,     'value': radon24h,    'scale': Sensor.SCALE_UNKNOWN})
                #values.append({'type': Sensor.WATT,        'value': radon24h,    'scale': Sensor.SCALE_POWER_WATT})
                #self.sensor.setSensorValues(values)
		#self.sensor.setSensorValue(Sensor.UNKNOWN, radon24h, Sensor.SCALE_UNKNOWN)

                
