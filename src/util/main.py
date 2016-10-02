#! /usr/bin/python
# -*- coding: utf-8 -*-
from logger import Logger
from parser import Parser
import util


def parse(parser,directory,files):
	for f in files:
		name = parser.parse(directory,f)
		if(name):
			parser.get_co(name)
		
def init():
	# initialize logger
	logger = Logger().get_logger()
	logger.info("Initializing...")
	
	# Parser
	parser = Parser()
	
	directory = "teste"
	files =  util.get_xml("teste")
	parse(parser,directory,files)

	
	
	
if __name__=='__main__':
	init()