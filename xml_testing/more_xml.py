import lxml.etree as etree
path='pubmed_result_tighe.xml'
tree = etree.parse('pubmed_result_tighe.xml')
import pandas as pd
# for element in tree.iter():
#     print (element.tag)
#
# root = tree.getroot()


for obj in tree.xpath('//PubmedArticleSet/PubmedArticle/MedlineCitation/Article/ArticleTitle'):
    print (obj.text)

tree.xpath('//Article/ArticleTitle')
