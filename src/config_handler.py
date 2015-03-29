#!/usr/bin/env python3
import json
CONFIG_NAME = "config.json"
loaded = {}

def load_config(name):
	global loaded
	if name in loaded:
		return loaded[name]
	with open(name) as confile:
		conf = conffile.read()
	conf = json.loads(conf)
	loaded[name] = conf
	return conf

def get_from_config(name, value):
	conf = load_config(name)
	return conf[value]

