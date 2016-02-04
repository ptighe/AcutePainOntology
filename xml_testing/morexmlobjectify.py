from lxml import objectify
import pandas as pd

path='pubmed_result_tighe.xml'
xml = objectify.parse(open(path))
root = xml.getroot()
parents = root.getchildren()

parents

for elem in xml.iter(tag='AbstractText'):
    print (elem.tag, elem.attrib, elem.text)


df = pd.DataFrame(columns=('PMID','PubDateYear','PubDateMonth','JournalTitle',
                           'JournalAbbrev','ArticleTitle','AbstractText'))