# -*- coding: utf-8 -*-


from base import Plugin, implements
from telldus.web import IWebReactHandler

class Webinterface(Plugin):
	implements(IWebReactHandler)

	@staticmethod
	def getReactComponents():
		return {
			'webinterface': {
				'title': 'Webinterface example',
				'script': 'webinterface/welcome.js',
				'tags': ['menu'],
			}
		}
