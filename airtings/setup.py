#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name='Radon sensor',
	version='1.3',
	author='Patrik Thalin',
	author_email='patrik@thalin.se',
	color='#2c3e50',
	description='Airting Wave Radon sensor plugin',
	icon='radon.png',
	long_description="""
		This plugin is read Radon values from a server that pulls data from Airthings Wave over Bluetooth.
	""",
	packages=['radon'],
	package_dir = {'':'src'},
	entry_points={ \
		'telldus.startup': ['c = radon:Radon [cREQ]']
	},
	extras_require = dict(cREQ = 'Base>=0.1\nTelldus>=0.1'),
)
