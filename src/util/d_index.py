#!/usr/bin/python
# -*- coding: utf-8 -*-

import util


def net(p,info):
	network = []
	author_set = []
	for item in p:
		authors = item.get('AUTHORS')
		net = []
		for a in authors:
			a = a.get('CITATION-NAMES').split(";")
			for x in a:
				x = x.upper()
				#if(x not in info):
				net.append(x.strip())
				if(x not in author_set):
					author_set.append(x.strip())
		if(len(net)>0):
			network.append(net)
	
	return network,author_set

def pub(net,i,j,k):
	all = [0,0,0]
	
	if(isinstance(i, unicode)):
		i = {i}
	if(isinstance(j, unicode)):
		j = {j}
	if(isinstance(k, unicode)):
		k = {k}
	for n in net:
		ok_i =  any(x in n for x in i)
		ok_j =  any(x in n for x in j)
		ok_k =  any(x in n for x in k)
		if(ok_i and ok_j and ok_k):
			all[0] = all[0] + 1
		elif(ok_i and ok_k and not ok_j):
			all[1] = all[1] + 1
		elif(ok_k and ok_j and not ok_i):
			all[2] = all[2] + 1
	return all

def main(I_name,J_name):
	print I_name
	print J_name
	
	I = util.load_json(I_name)
	I_articles = I.get('ARTICLES')
	I_size = len(I_articles)
	I_info = I.get('GENERAL-INFORMATION').get('CITATION-NAMES').split(";")
	I_info = [x.upper() for x in I_info]
	
	
	
	J = util.load_json(J_name)
	J_articles = J.get('ARTICLES')
	J_size = len(J_articles)
	J_info = J.get('GENERAL-INFORMATION').get('CITATION-NAMES').split(";")
	J_info = [x.upper() for x in J_info]
	
	
	I_net, I_co = net(I_articles,I_info)
	J_net, J_co = net(J_articles,J_info)
	inter = set(I_co).intersection(J_co)
	
	to_remove = []
	for item in inter:
		if(item in I_info or item in J_info):
			to_remove.append(item)
	inter = list(set(inter) - set(to_remove))
	
	if(len(inter)<=0):
		print "NO INTERSECTION"
		exit(1)

	total = 0
	for author in inter:
		p = pub(I_net+J_net,I_info,J_info,author)
		print p
		try:
			w = 1-((p[0]+p[1])/float((p[0]+p[1]+p[2])))
		except:
			w = 0
			print "error"
		total += w
	d = (I_size/float(J_size)) * (total/float(len(inter)))
	print float("{0:.4f}".format(d))
	
if __name__=='__main__':
	import os
	import itertools
	
	files = []
	
	for file in os.listdir("."):
		if file.endswith('.json'):
			files.append(file)
	
	all_comb = itertools.combinations(files,2)
	for item in all_comb:
		main(item[0],item[1])
	
	
	#main()
	
	
	
