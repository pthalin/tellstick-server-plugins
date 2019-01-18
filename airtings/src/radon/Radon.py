# -*- coding: utf-8 -*-

import math
import time
import urllib2

from base import Application, Plugin
from telldus import DeviceManager, Sensor

class RadonSensor(Sensor):
	'''All sensors exported must subclass Sensor

	Minimal function to reimplement is:
	localId
	typeString
	'''
	@staticmethod
	def localId():
		'''Return a unique id number for this sensor. The id should not be
		globally unique but only unique for this sensor type.
		'''
		return 5

	@staticmethod
	def typeString():
		'''Return the sensor type. Only one plugin at a time may export sensors using
		the same typestring'''
		return 'radon'

	def updateValue(self):
		"""setRadonSensor value constantly."""
		#xVal = time.time()/60%62
		# This is dummy data for testing sine wave
		#radon = round(math.sin(xVal*0.1)*25+50, 2)
                content = urllib2.urlopen("http://192.168.1.164:8888").read()
                data = content.split(',')
                radon = float(data[3])
		self.setSensorValue(Sensor.UNKNOWN, radon, Sensor.SCALE_UNKNOWN)

class Radon(Plugin):
	'''This is the plugins main entry point and is a singleton
	Manage and load the plugins here
	'''
	def __init__(self):
		# The devicemanager is a globally manager handling all device types
		self.deviceManager = DeviceManager(self.context)

		# Load all devices this plugin handles here. Individual settings for the devices
		# are handled by the devicemanager
		self.sensor = RadonSensor()
		self.deviceManager.addDevice(self.sensor)

		# When all devices has been loaded we need to call finishedLoading() to tell
		# the manager we are finished. This clears old devices and caches
		self.deviceManager.finishedLoading('radon')

		Application().registerScheduledTask(self.updateValues, minutes=10, runAtOnce=True)

	def updateValues(self):
		self.sensor.updateValue()
