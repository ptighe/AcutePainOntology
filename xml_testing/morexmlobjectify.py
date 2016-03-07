from lxml import objectify
import pandas as pd

path='xml_testing/pubmed_result_tighe.xml'
tree = objectify.parse(open(path))
root = tree.getroot()
parents = root.getchildren()

parents

for elem in tree.iter(tag='AbstractText'):
    print (elem.tag, elem.attrib, elem.text)

for elem in tree.iterfind('//Abstract/AbstractText'):
    print (elem.tag,elem.text)


for elem in tree.iterfind('//PMID'):
    print (elem.tag,elem.text)

for elem in tree.iterfind('//Article/ArticleTitle'):
    print (elem.tag,elem.text)

for elem in tree.iterfind('//')

# root.getchildren()[0].getchildren()
#
# for child in root.getchildren()[0].getiterator():
#     print (child.tag)
#
# for child in root.getchildren()[0].getchildren()[1].getchildren():
#     print (child.tag)

pmid = tree.xpath('//PMID')[1]

for i in range(0,3):
    print (tree.xpath('//PMID')[i])



df = pd.DataFrame(columns=('PMID','PubDateYear','PubDateMonth','FirstAuthors','JournalTitle',
                           'JournalAbbrev','ArticleTitle','AbstractText'))

dfsimple = pd.DataFrame(columns=('PMID','ArticleTitle','AbstractText'))

for i in range(len(parents)):
    dfsimple.loc[i,'PMID']= tree.xpath('//PMID')[i]
    dfsimple.loc[i,'ArticleTitle']=tree.xpath('//Article/ArticleTitle')[i]
    dfsimple.loc[i,'AbstractText']=tree.xpath('//Abstract/AbstractText')[i]

print dfsimple
    # pm_id = tree.xpath('//PMID')[i]
    # article_title = tree.xpath('//Article/ArticleTitle')[i]
    # abstract_text = tree.xpath('//Abstract/AbstractText')[i]
