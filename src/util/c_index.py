#!/usr/bin/python
# -*- coding: utf-8 -*-


import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

import util


def construct_graph(co_dict,co_co_dict):
	
	G=nx.Graph()
	
	for k in co_dict.iterkeys():
		G.add_node(k)
		print k
		
	nx.draw(G, with_labels = True)
	plt.show()
	

def calculate(co_dict,co_co_dict):
	
	s = []
	
	for k,v in co_dict.iteritems():
		try:
			co = co_co_dict[k]
		# maybe there is not an id
		except:
			continue
		
		strength = v * sum(co.values())
		s.append(strength)
	
	s.sort(reverse=True)
	
	foo = 0
	
	if(len(s)<=0):
		return foo
	
	
	
	for i in s:
		if(i>=foo):
			foo +=1
		else:
			break
		
	return foo
		


def graph_it(input_file):
	json_file = util.load_json(input_file)
	co_dict = defaultdict(int)
	co_co_dict = {}
	
	master_id = json_file.get('GENERAL-INFORMATION').get('ID')
	
	articles = json_file.get('ARTICLES')
	
	for a in articles:
		for co in a.get('AUTHORS'):
			co_id = co.get('ID')
			if(co_id != master_id and co_id):
				co_dict[co_id]+=1
	
	co_dict = dict(co_dict)
	
	
	for key in co_dict.iterkeys():
		
		tmp_dict = defaultdict(int)
		for a in articles:
			pre_list = [x.get('ID') for x in a.get('AUTHORS')]
			if(key in pre_list):
				for co in a.get('AUTHORS'):
					co_id = co.get('ID')
					if(co_id != key and co_id):
						tmp_dict[co_id]+=1

		tmp_dict = dict(tmp_dict)
		if(len(tmp_dict)>0):
			co_co_dict[key] = tmp_dict
	
	#construct_graph(co_dict,co_co_dict)
	print calculate(co_dict,co_co_dict)
		
	
	
	
	

def main():
	#parser('../../resources/curriculo4.xml')
	graph_it('../../resources/json/ViktorDodonov.json')

if __name__=='__main__':
	main()