#!/usr/bin/env python3
import os
import json
VISITED_NAME = "visited.json"
CONFIG_NAME = "config.json"


class ConfigHandler(object):
	def __init__(self):
		self.cached = {}

	def	from_config(self, name, value=None):
		"""
		Loads a config with the given name.
		Caches the configs on load, and just returns the cached version then.
		Arguments:
			name: The name of the config
			value: What value to retrieve
		Return:
			The value of config[value] or None
		"""
		conf = None
		if name in self.cached:
			conf = self.cached[name]
		else:
			if name in os.listdir("."):
				with open(name) as config_file:
					conf = json.loads(config_file.read())
				self.cached[name] = conf
		if conf is not None:
			if value is None:
				return conf
			else:
				return conf[value]



# Gonna do this like the random module does, having a global config handler class
_hand = ConfigHandler()
from_config = _hand.from_config
