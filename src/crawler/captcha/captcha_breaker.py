#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cv2
import Image
import numpy as np

from pytesseract import image_to_string as tesseract
from matplotlib import pyplot as plt


SEP = os.path.sep

def load_png(d):
	
	files = {}
	
	for f in os.listdir(d):
		if f.endswith('.png'):
			t = cv2.imread(d+SEP+f,0)
			files[f] = t
	return files


def match(i,t):
	
	pts = []
	
	img = cv2.imread(i)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_,gray = cv2.threshold(gray, 231, 255, cv2.THRESH_BINARY_INV)
	
	#template = cv2.imread(t,0)
	template = t
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.75
	
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
		pts.append(pt[0])
		
	
	return pts
	
def break_it(c):
	cd = os.path.dirname(os.path.abspath(__file__))
	files = load_png(cd+"/alpha/")
	result = {}
	
	for v,k in files.iteritems():
		tmp = match(c,k)
		if(len(tmp)>0):
			for t in tmp:
				result[t] = v
	
	captcha = ""
	
	for v in sorted(result):
		captcha += str(result.get(v).split(".png")[0]).upper()
	
	return captcha


# test
def main():
	
	files = load_png("alpha")
	result = {}
	
	for v,k in files.iteritems():
		tmp = match("captcha5.png",k)
		if(len(tmp)>0):
			for t in tmp:
				result[t] = v
	
	captcha = ""
	
	for v in sorted(result):
		captcha += str(result.get(v).split(".png")[0]).upper()
	
	print captcha
				
	
if __name__=='__main__':
	main()