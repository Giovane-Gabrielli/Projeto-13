#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cv2
from selenium import webdriver
from time import sleep

from captcha.captcha_breaker import break_it

user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"

def my_list(p):
	with open('my_list.txt','a+') as f:
		for i in p:
			f.write(i+'\n')
def new_list(p):
	with open('new_list.txt','a+') as f:
		f.write(p+'\n')
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
		
		img = driver.find_element_by_xpath("//img[@alt='Captcha']")
		
		driver.save_screenshot(ss)
		print "screenshot..."
		
		location = img.location
		size = img.size
		captcha = solve_captcha(ss, location, size,"captcha/captcha.png")
		
		if(captcha):
			box = driver.find_element_by_id('informado')
			box.send_keys(captcha)
			sleep(3)
			driver.find_element_by_id('btn_validar_captcha').click()
			sleep(3)

			
			# when there is no id
			"""
			opt = driver.find_element_by_class_name('informacoes-autor')
			for items in opt.find_elements_by_tag_name('li'):
				if("este CV:" in items.text):
					new_list(items.text.split("este CV: ")[1].strip())
					break
			"""
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
	
def scholarship(driver):
	driver.find_element_by_id('filtro0').click()
	driver.find_element_by_id('checkbox1A').click()
	driver.find_element_by_id('checkbox1B').click()
	driver.find_element_by_id('checkbox1C').click()
	driver.find_element_by_id('checkbox1D').click()
	driver.find_element_by_id('checkbox2').click()
	driver.find_element_by_id('preencheCategoriaNivelBolsa').click()

def physics(driver):
	driver.find_element_by_id('filtro4').click()
	opt = driver.find_element_by_id('codigoGrandeAreaAtuacao')
	
	for option in opt.find_elements_by_tag_name('option'):
		if option.get_attribute('value') == "10000003":
			option.click()
			break
		
	sleep(0.5)
	opt2 = driver.find_element_by_id('codigoAreaAtuacao')
	for option in opt2.find_elements_by_tag_name('option'):
		if option.get_attribute('value') == "10500006":
			option.click()
			break
		
	sleep(0.5)
	

	driver.execute_script("""
	aplicarFiltroAtuacao();
	fecharFiltro(4);
	""")
	
def all_pages(driver):
	i=2
	while(True):
		
		l = []
		opt = driver.find_element_by_class_name('resultado')
		for ol in opt.find_elements_by_tag_name('ol'):
			for li in ol.find_elements_by_tag_name('li'):
				l.append(li.find_element_by_css_selector('a').get_attribute('href'))
				print i,li.find_element_by_css_selector('a').get_attribute('href')
		if(i>19 and (i-1)%10.0==0):
			links = driver.find_elements_by_partial_link_text('próximo')
			for link in links:
				link.click()	
				break
		else:
			links = driver.find_elements_by_partial_link_text(str(i))
			for link in links:
				link.click()	
				break
			
		i+=1
		my_list(l)
		sleep(3)

def get_them(p):
	profile = webdriver.FirefoxProfile()
	profile.set_preference("general.useragent.override", user_agent)
	driver = webdriver.Firefox(firefox_profile=profile)
	
	try:
		driver.get(p)
		scholarship(driver)
		physics(driver)
		driver.find_element_by_id('botaoBuscaFiltros').click()
		all_pages(driver)
		
		
	except Exception as e:
		print e

if __name__=='__main__':
	"""
	import os
	
	d = "../../resources/coauthors/"
	for f in os.listdir(d):
	
		pages = load(d+f)
		
		for page in pages:
			print page
			go(page)
	"""
	# TODO
	# crawler
	#get_them('http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar')
	
	pages = load('lattes.txt')
	for page in pages:
		print page
		go(page)
