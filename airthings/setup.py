#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name='Airtings Wave',
	version='1.0',
	author='Patrik Thalin',
	author_email='patrik@thalin.se',
	color='#2c3e50',
	description='Airtings Wave plugin',
	icon='radon.png',
	long_description="""
		Reads radon values from a server 
                that get values over Bluetooth. 
	""",
	packages=['radon'],
	package_dir = {'':'src'},
	entry_points={ \
		'telldus.startup': ['c = radon:Radon [cREQ]']
	},
	extras_require = dict(cREQ = 'Base>=0.1\nTelldus>=0.1'),
)
