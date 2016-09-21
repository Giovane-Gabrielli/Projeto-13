#! /usr/bin/python
# -*- coding: utf-8 -*-

import json

def load_json(file):
	with open(file) as f:
		j = json.load(f)
	return j

# convert data to json
def data2json(name, data):
	with open(name, 'w') as f:
		json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)