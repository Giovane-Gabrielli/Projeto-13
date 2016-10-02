#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
from logger import Logger
import xml.etree.ElementTree as ET

# global
SEP = os.path.sep
resources = str(os.path.abspath("../../resources/"))
js = str(os.path.abspath("../../resources/json"))
xml = str(os.path.abspath("../../resources/xml"))
coauthors = str(os.path.abspath("../../resources/coauthors"))

PATH = {
	'RESOURCES': resources,
	'JSON': js,
	'XML' : xml,
	'COAUTHORS' : coauthors,
	
	}

def load_json(path,file_name):
	try:
		name = PATH['JSON']+SEP+path+SEP+file_name
		with open(name) as f:
			j = json.load(f)
		return j
	except Exception as e:
		logger = Logger().get_logger()
		logger.warning(e)

# convert data to json
def data2json(file_name, data):
	
	name = PATH['JSON']+SEP+file_name
	print name
	try:
		os.mkdir(name, 0755)
		
	except Exception as e:
		logger = Logger().get_logger()
		logger.warning(e)
		
	os.chdir(name)
	name = name.split(SEP)[-1]
	with open(name+'.json', 'w') as f:
		json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
		
def load_xml(path,file_name):
	try:	
		name = PATH['XML']+SEP+path+SEP+file_name
		tree = ET.parse(name)
		return tree
		
	except Exception as e:
		logger = Logger().get_logger()
		logger.warning(e)

def get_xml(name):
	try:
		files = []
		name = PATH['XML']+SEP+name
		for f in os.listdir(name):
			if f.endswith('.xml'):
				files.append(f)
		return files
	except Exception as e:
		logger = Logger().get_logger()
		logger.warning(e)

def write_coauthors(name,ids,lattes=None):
	try:
		name = PATH['COAUTHORS']+SEP+name
		with open(name,'w') as f:
			for i in ids:
				f.write(lattes+i+'\n')
	except Exception as e:
		logger = Logger().get_logger()
		logger.warning(e)
	