#!/usr/bin/env python3
import os
import json
LOGIN_NAME = "credentials.json"
CONFIG_NAME = "config.json"


class ConfigHandler(object):
	def __init__(self):
		self.cached = {}

	def	from_config(self, name, value):
		"""
		Loads a config with the given name.
		Caches the configs on load, and just returns the cached version then.
		Arguments:
			self: The Class, duh.
			name: The name of the config
			value: What value to retrieve
		Return:
			The value of config[value] or None
		"""
		if name in self.cached:
			return self.cached[name][value]
		if name in os.listdir("."):
			with open(name) as config_file:
				conf = json.loads(config_file.read())
			self.cached[name] = conf
			return conf[value]


# Gonna do this like the random module does, having a global config handler class
_hand = ConfigHandler()
from_config = _hand.from_config
