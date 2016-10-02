#! /usr/bin/python
# -*- coding: utf-8 -*-


import util

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



class Parser():

	# parse all the shit
	def parse(self,path,file_name):
		
		tree = util.load_xml(path,file_name)
		
		root = tree.getroot()
		
		data = {}
		
		# STORE THE GENERAL INFORMATIONS
		# SUCH AS ID, NAME AND CITATION NAMES
		
		general_info = {}
		try:
			general_info['ID'] = root.get('NUMERO-IDENTIFICADOR').encode('utf-8')
			info = root.find('DADOS-GERAIS')
			general_info['COMPLETE-NAME'] = info.get('NOME-COMPLETO').encode('utf-8')
			name =  info.get('NOME-COMPLETO').replace(" ","")
			general_info['CITATION-NAMES'] = info.get('NOME-EM-CITACOES-BIBLIOGRAFICAS').encode('utf-8')#.split(",")
			
			general_info['PHD-BEGGINING'] = info.find('FORMACAO-ACADEMICA-TITULACAO').find('DOUTORADO').get('ANO-DE-INICIO')
			general_info['PHD-ENDING'] = info.find('FORMACAO-ACADEMICA-TITULACAO').find('DOUTORADO').get('ANO-DE-CONCLUSAO')
			
			data['GENERAL-INFORMATION'] = general_info
		except:
			#fail(str(file))
			return 
		
		articles_data = []
		# CONTINUE
		for child in root:
			
			ok = next((child.tag for x in white_list if x in child.tag),False)
			#print child.tag
			
			# GO FURTHER
			if(ok):
				articles = []
				self.rem(child, 0, articles)
				articles_data = articles_data+articles
				
		data['ARTICLES'] = articles_data
		util.data2json(name,data)
		return name

	# FIND ALL THE AUTHORS, BABY
	def rem(self,node, t, articles):
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
				self.rem(child, t+1, articles)


	# RECEIVES A JSON FILE
	def get_co(self,input_file):

		ids = []
		lattes = 'http://buscatextual.cnpq.br/buscatextual/download.do?metodo=apresentar&idcnpq='
		name = input_file + '.txt'

		
		json_file = util.load_json(input_file,input_file+'.json')
		author_id = json_file.get('GENERAL-INFORMATION').get('ID')
		
		articles = json_file.get('ARTICLES')
		
		for a in articles:
			for author in a.get('AUTHORS'):
				current_id = author.get('ID')
				if(current_id):
					ids.append(current_id)
		ids = list(set(ids))
		try:
			ids.remove(author_id)
		except:
			pass
		
		util.write_coauthors(name,ids,lattes=lattes)

		#return ids
	
	

def main():
	#d = "../../resources/xml/test/"
	p = Parser()
	p.parse(d,files[0])
	"""for f in files:
		print f
		name = parser(d+f,'../../resources/json/')
		if(name):
			get_co(name)"""

if __name__=='__main__':
	main()
