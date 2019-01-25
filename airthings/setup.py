#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name='Airtings Wave Radon sensor',
	version='1.4',
	author='Patrik Thalin',
	author_email='patrik@thalin.se',
	color='#2c3e50',
	description='Airtings Wave Radon sensor plugin',
	icon='radon.png',
	long_description="""
		This plugin reads Radon values from a server (Raspberry Pi 3) that pulls data from a Wave device over Bluetooth. 
	""",
	packages=['radon'],
	package_dir = {'':'src'},
	entry_points={ \
		'telldus.startup': ['c = radon:Radon [cREQ]']
	},
	extras_require = dict(cREQ = 'Base>=0.1\nTelldus>=0.1'),
)
