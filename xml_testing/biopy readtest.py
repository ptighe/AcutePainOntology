from Bio import Entrez
file = 'pubmed_result_tighe.xml'


handle = open('pubmed_result_tighe.xml')

record = Entrez.read(handle)