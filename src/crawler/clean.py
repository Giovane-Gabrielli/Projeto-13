#! /usr/bin/python
# -*- coding: utf-8 -*-

if __name__=='__main__':
	li = []
	with open('my_list.txt','r') as f:
		for l in f:
			l=l.replace("javascript:abreDetalhe('","")
			l=l.split("'")[0]
			print "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id="+l