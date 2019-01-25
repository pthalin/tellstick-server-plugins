# -*- coding: utf-8 -*-

import math
import time
import urllib2

from base import Application, Plugin, ConfigurationString, configuration
from telldus import DeviceManager, Sensor

class RadonSensor(Sensor):

	@staticmethod
	def localId():
                #todo: use  id codecs.encode(device.mac, "hex_codec") 
		return 5
        
	@staticmethod
	def typeString():
		return 'radon'

	def updateValue(self):
                host_url =  'http://' + self.config('serverAddress')
                content = urllib2.urlopen(host_url).read()
                data = content.split(',')
                #timeStamp   = float(data[0])
                #temperature = float(data[1])
                #humidity    = float(data[1])
                radon24h    = float(data[3])
                #radonLong   = float(data[4])
		self.setSensorValue(Sensor.UNKNOWN, radon24h, Sensor.SCALE_UNKNOWN)
                
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
		self.sensor = RadonSensor()
		self.deviceManager.addDevice(self.sensor)
		self.deviceManager.finishedLoading('radon')
		Application().registerScheduledTask(self.updateValues, minutes=10, runAtOnce=True)

	def updateValues(self):
		self.sensor.updateValue()
