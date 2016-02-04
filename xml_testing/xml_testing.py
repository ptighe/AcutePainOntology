from Bio import Entrez

handle = open('pubmed_result_tighe.xml')
records = Entrez.parse(handle)

for record in records:
    print(record['MedlineCitation']['Article']['ArticleTitle'])


#

