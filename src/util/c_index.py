#!/usr/bin/python
# -*- coding: utf-8 -*-

import util


def graph_it(input_file):
	json_file = util.load_json(input_file)


def main():
	#parser('../../resources/curriculo4.xml')
	graph_it('../../resources/json/ViktorDodonov.json')

if __name__=='__main__':
	main()