#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = None
class Logger():
	def __init__(self):
		
		global logger
		
		# fake singleton
		if(logger==None):
			self.name = 'log_horizon'
			self.logger = logging.getLogger(self.name)
			
			self.logger.setLevel(logging.DEBUG)
			self.fh = logging.FileHandler('log.log')
			self.fh.setLevel(logging.DEBUG)
			
			self.ch = logging.StreamHandler()
			self.ch.setLevel(logging.ERROR)
			
			self.formatter = logging.Formatter('%(name)s - %(asctime)s - %(filename)s - %(levelname)s - %(message)s')
			self.ch.setFormatter(self.formatter)
			self.fh.setFormatter(self.formatter)
			
			self.logger.addHandler(self.ch)
			self.logger.addHandler(self.fh)
			
			logger = self.logger
			
	def get_logger(self):
		return logger