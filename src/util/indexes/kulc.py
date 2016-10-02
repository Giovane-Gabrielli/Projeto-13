#! /usr/bin/python

import util

# p - number of papers
# i - author, j- co-autor
# k - initial year, t - final year

def one_iteration_kulc (p_i, p_j, p_ij,year):
    try:
	x =(p_ij)/2.0
	y = (1/float(p_i))
	z = (1/float(p_j))
	atual_iteration = (x * (y+z))
	print "Iteration | ",year," |" ,atual_iteration
 	print p_i,p_j,p_ij
	print
	return atual_iteration
    except:
	print "Iteration | ",year," |", 0.
 	print p_i,p_j,p_ij
	print
	return 0

def get_p_specific_one_year (name_i, name_j, year):
    #print name_i
    #print name_j
    year =  unicode(year)
    ij_size = 0

    i = util.load_json(name_i)
    i_articles =  i.get('ARTICLES')
    i_size = 0
    j = util.load_json(name_j)

    j_ID = j.get('GENERAL-INFORMATION').get('ID')
    
    for article in i_articles:
        if (article.get('GENERAL-INFORMATION').get('DATE')==year):
	    i_size+=1
            authors = article.get('AUTHORS')
            for author in authors:
                if (j_ID == author.get('ID')):
                    ij_size = ij_size +1
                    
    return i_size, ij_size


def calc_kulc (i, j, k, t):

    kulc_valor = 0
    p_i_total = 0
    p_ij_total = 0
    p_j_total  = 0
    
    k_true = 0
    k_year = k
    #print 'before calc_kulc for'
    
    for k1 in range (k,t+1):
	
        p_i, p_ij = get_p_specific_one_year(i, j, k1)
        p_j, p_ji = get_p_specific_one_year(j, i, k1)
        
        p_i_total += p_i
        p_ij_total += p_ij
        p_j_total += p_j
        #print p_i,p_j,p_ij
        atual_iteration_valor = one_iteration_kulc(p_i_total, p_j_total, p_ij_total,k1)
        #kulc_valor = kulc_valor + atual_iteration_valor
        kulc_valor = atual_iteration_valor
        
        if(p_ij != 0):
		k_true = kulc_valor
		k_year = k1

    #print kulc_valor

    return float("{0:.4f}".format(kulc_valor)),k_year

if __name__ == '__main__':

    name_i = '../../resources/json/ViktorDodonov.json'
    i = util.load_json(name_i)
    i_phd = i.get('GENERAL-INFORMATION').get('PHD-BEGGINING')
    
    k, year= calc_kulc(name_i,\
	    '../../resources/json/MarcosCesardeOliveira.json', int(i_phd), 2017)
    print
    print "Kulczynski index:",k
    print "Last year:", year
    print

    # main()
