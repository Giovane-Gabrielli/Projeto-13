#! /usr/bin/python
# -*- coding: utf-8 -*-

if __name__=='__main__':
	li = []
	with open('new_list1.txt','r') as f:
		for l in f:
			"""
			l=l.replace("javascript:abreDetalhe('","")
			l=l.split("'")[0]
			print "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id="+l
			"""
			if(l in li):
				print l
			else:
				li.append(l)