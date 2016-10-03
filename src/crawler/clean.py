#! /usr/bin/python
# -*- coding: utf-8 -*-

if __name__=='__main__':
	li = []
	with open('new_list.txt','r') as f:
		for l in f:
			"""
			l=l.replace("javascript:abreDetalhe('","")
			l=l.split("'")[0]
			print "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id="+l
			"""
			lattes = 'http://buscatextual.cnpq.br/buscatextual/download.do?metodo=apresentar&idcnpq='
			li.append(l.split('/')[-1].strip())
	li2 = []
	with open('done.txt','r') as f:
		for l in f:
			"""
			l=l.replace("javascript:abreDetalhe('","")
			l=l.split("'")[0]
			print "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id="+l
			"""
			lattes = 'http://buscatextual.cnpq.br/buscatextual/download.do?metodo=apresentar&idcnpq='
			li2.append(l.split('.zip')[0])
			
	for i in li:
		if i not in li2:
			print i