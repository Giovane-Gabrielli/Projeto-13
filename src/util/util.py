#! /usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import json

# main information
white_list = [u'PRODUCAO']

# specific information
black1 = u'DADOS-BASICOS'
black2 = u'AUTORES'
black_list = [black1,black2]

# wtf
gray1 = u'TITULO'
gray2 = u'ANO'
gray_list = [gray1,gray2]

# convert data to json
def data2json(name, data):
	with open(name, 'w') as f:
		json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

# parse all the shit
def parser(file):
	try:
		tree = ET.parse(file)
	except Exception as e:
		print e
		exit(1)
	
	root = tree.getroot()
	
	data = {}
	
	# STORE THE GENERAL INFORMATIONS
	# SUCH AS ID, NAME AND CITATION NAMES
	
	general_info = {}
	general_info['ID'] = root.get('NUMERO-IDENTIFICADOR').encode('utf-8')
	info = root.find('DADOS-GERAIS')
	general_info['COMPLETE-NAME'] = info.get('NOME-COMPLETO').encode('utf-8')
	name = info.get('NOME-COMPLETO').replace(" ","") + ".json"
	general_info['CITATION-NAMES'] = info.get('NOME-EM-CITACOES-BIBLIOGRAFICAS').encode('utf-8')#.split(",")
	
	data['GENERAL-INFORMATION'] = general_info
	articles_data = []
	# CONTINUE
	for child in root:
		
		ok = next((child.tag for x in white_list if x in child.tag),False)
		#print child.tag
		
		# GO FURTHER
		if(ok):
			articles = []
			rem(child, 0, articles)
			articles_data = articles_data+articles
			
	data['ARTICLES'] = articles_data
	data2json(name,data)

# FIND ALL THE AUTHORS, BABY
def rem(node, t, articles):
	ram = node.findall(u'AUTORES')
	if(ram):
		#print node.tag
		article = {}
		authors = []
		for child in node:
			
			ok = next((child.tag for x in black_list if x in child.tag),False)
			
			if(ok):
				
				# IF GENERAL INFORMATION
				if(black1 in child.tag):
					# PUBLICATION GENERAL INFORMATION
					general_info = {}
					for grand_child in child.keys():
						if(gray1 in grand_child and u'ING' in grand_child):
							general_info['ENGLIGH-TITLE'] = child.get(grand_child).encode('utf-8')
						elif(gray1 in grand_child and u'ING' not in grand_child):
							general_info['PORTUGUESE-TITLE'] = child.get(grand_child).encode('utf-8')
						elif(gray2 in grand_child):
							general_info['DATE'] = child.get(grand_child).encode('utf-8')
					article['GENERAL-INFORMATION'] = general_info
				else:
					author = {}
					author['COMPLETE-NAME'] = child.get('NOME-COMPLETO-DO-AUTOR').encode('utf-8')
					author['CITATION-NAMES'] = child.get('NOME-PARA-CITACAO').encode('utf-8')#.split(",")
					try:
						author['ID'] = child.get('NRO-ID-CNPQ').encode('utf-8')
					except:
						author['ID'] = ""
						
					authors.append(author)
				#print t*'\t' + child.tag, child.attrib
				#print "\n\n\n"
				#pass
		article['AUTHORS'] = authors
		articles.append(article)
	else:
		#print t*'\t' + node.tag
		
		for child in node:
			rem(child, t+1, articles)

def load_json(file):
	with open(file) as f:
		j = json.load(f)
	return j

# RECEIVES A JSON FILE
def get_co(input_file):
	ids = []
	lattes = 'http://lattes.cnpq.br/'
	name = '../../resources/coauthors/'+input_file.split('/')[-1].replace('.json','.txt')
	
	json_file = load_json(input_file)
	author_id = json_file.get('GENERAL-INFORMATION').get('ID')
	
	articles = json_file.get('ARTICLES')
	
	for a in articles:
		for author in a.get('AUTHORS'):
			current_id = author.get('ID')
			if(current_id):
				ids.append(current_id)
	ids = list(set(ids))
	ids.remove(author_id)
	
	with open(name,'w') as f:
		for i in ids:
			f.write(lattes+i+'\n')
	
	#return ids
	
	

def main():
	#parser('../../resources/curriculo4.xml')
	ids = get_co('../../resources/json/ViktorDodonov.json')

if __name__=='__main__':
	main()
