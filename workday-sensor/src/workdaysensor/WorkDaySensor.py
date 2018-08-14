
from datetime import date, datetime
import time
import pytz
from base import Plugin, Settings, Application, configuration, ConfigurationList
import holidays
from telldus import DeviceManager, Device
from iso3166 import countries
import logging

# pylint: disable=E0211,E0213,W0622,W0312

__name__ = 'countryList'

class WorkDay(Device):

	def __init__(self):
		super(WorkDay, self).__init__()

	def _command(self, action, value, success, failure, **kwargs):
    		logging.debug('Sending command %s to dummy device', action)
		success()

	def localId(self):
    		return 1
        
	def typeString(self):
            return 'workday'

@configuration(
	countryList=ConfigurationList(
		defaultValue=["Argentina", "Australia", "Austria", "Belgium", "Canada", "Colombia", "Czech", "Denmark", "England",
            "Finland", "France", "Germany", "Hungary", "India", "Ireland", "Isle of Man", "Italy", "Japan", "Mexico", "Netherlands",
            "NewZealand", "Northern Ireland", "Norway", "Polish", "Portugal", "PortugalExt", "Scotland", "Slovenia", "Slovakia",
            "South Africa", "Spain", "Sweden", "Switzerland", "UnitedKingdom", "UnitedStates", "EuropeanCentralBank", "Wales"
        ],
		title='Country List',
		description='List of all supported countries',
	)
)

class WorkDaySensor(Plugin):

    def __init__(self):
		self.s = Settings('telldus.scheduler')
		self.timezone = self.s.get('tz', 'UTC')
		self.device = WorkDay()
		self.deviceManager = DeviceManager(self.context)
		self.deviceManager.addDevice(self.device)
		self.deviceManager.finishedLoading('workday')
		Application().registerScheduledTask(self.checkDay, minutes=1, runAtOnce=True)

    def checkDay(self):
        country_code = self.countryCode();
        date_time = datetime.now(pytz.timezone(self.timezone))
        try:
            country_holidays = holidays.CountryHoliday(country_code)
        except country_code == "":
            pass
        except:
            country_holidays = holidays.CountryHoliday(countries.get(country_code).alpha3)
        if date(date_time.year, date_time.month, date_time.day) in country_holidays and date_time.hour==00 and date_time.minute==01 and self.countryCode()!="":
    	    self.deviceAction(2)
        elif date_time.hour==00 and date_time.minute==01:
            self.deviceAction(1)

    def deviceAction(self,action):
        self.device.command(action=action)

    def countryCode(self):
        countr_code=""
        for countrycode in pytz.country_timezones:
            timezones = pytz.country_timezones[countrycode]
            for timezone in timezones:
                if timezone == self.timezone:
                    countr_code = countrycode
        return countr_code
