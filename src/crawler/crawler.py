#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cv2
from selenium import webdriver
from time import sleep

from captcha.captcha_breaker import break_it

user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"



def fail(p):
	with open('fail.txt','a+') as f:
		f.write(p+'\n')

def done(p):
	with open('done.txt','a+') as f:
		f.write(p+'\n')

def load(file):
	l = []
	with open(file,"r") as f:
		for line in f:
			l.append(line.strip())
	return l

def go(p):
	# config
	cd = os.path.dirname(os.path.abspath(__file__))
	
	profile = webdriver.FirefoxProfile()
	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting", False)
	profile.set_preference("browser.download.dir", cd+"/../../resources/xml/")
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")

	profile.set_preference("general.useragent.override", user_agent)
	
	# init
	driver = webdriver.Firefox(firefox_profile=profile)
	ss = 'captcha/screenshot.png'
	try:
		driver.get(p)
		sleep(2)
		
		img = driver.find_element_by_xpath("//img[@alt='Captcha']")
		
		driver.save_screenshot(ss)
		print "screenshot..."
		
		location = img.location
		size = img.size
		captcha = solve_captcha(ss, location, size,"captcha/captcha.png")
		
		if(captcha):
			box = driver.find_element_by_id('informado')
			box.send_keys(captcha)
			sleep(2)
			driver.find_element_by_id('btn_validar_captcha').click()
			sleep(5)
			driver.close()
			print "done!\n"
			done(p)
		else:
			driver.close()
			fail(p)
			return

		
		
	except Exception as e:
		print "lattes error.\n"
		print e
		driver.close()
		fail(p)
		return
		
	
	
def solve_captcha(i,location,size,c):
	try:
		img = cv2.imread(i)
		x,y = location['x'], location['y']
		w,h = size['width'], size['height']
		crop = img[y: y + h, x: x + w]
		
		cv2.imwrite(c,crop)
		print "captcha breaker..."
		captcha = break_it(c)
	
		return captcha
	
	except Exception as e:
		print e
	

	

if __name__=='__main__':
	pages = load("../../resources/coauthors/ViktorDodonov.txt")
	
	for page in pages:
		print page
		go(page)

