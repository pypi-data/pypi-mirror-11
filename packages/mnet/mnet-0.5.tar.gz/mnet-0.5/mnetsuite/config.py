#!/usr/bin/python

'''
	MNet Suite
	config.py

	Michael Laforest
	mjlaforest@gmail.com

	Copyright (C) 2015 Michael Laforest

	This program is free software; you can redistribute it and/or
	modify it under the terms of the GNU General Public License
	as published by the Free Software Foundation; either version 2
	of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import json

class mnet_config:
	host_domains	= []
	snmp_creds		= []
	exclude_subnets	= []
	allowed_subnets	= []

	def __init__(self):
		return

	def load(self, filename):
		# load config
		json_data = self._load_json_conf(filename)
		if (json_data == None):
			return 0

		self.host_domains		= json_data['domains']
		self.snmp_creds			= json_data['snmp']
		self.exclude_subnets	= json_data['exclude']
		self.allowed_subnets	= json_data['subnets']

		return 1

	def _load_json_conf(self, json_file):
		json_data = None

		try:
			json_data = json.loads(open(json_file).read())

		except:
			print('Invalid JSON file or file not found.')
			return None

		return json_data

