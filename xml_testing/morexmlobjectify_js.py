import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from lxml import objectify
import pandas as pd
import os

os.getcwd()
os.chdir('xml_testing')
#Function to convert Affiliation to state and country
def stateNcountry(affilation):    
    state = []
    country = []
    for i in affilation:
        words = str(i).split(" ")
        if '@' in words[-1]:
            words.pop()
        if len(words) >= 2:
            country.append(words.pop().rstrip('.').rstrip(',').rstrip(':').rstrip(';'))
            state.append(words.pop().rstrip('.').rstrip(',').rstrip(':').rstrip(';'))    
    return state,country

#Generating xml tree from xml file
path='pubmed_result_tighe.xml'
tree = objectify.parse(open(path))

# Initializing Dataframe
author_df = pd.DataFrame(columns=('PMID','LastName','FirstName','State', 'Country'))
index = 0

# Converting xml data into Panda dataframe
for i in tree.xpath('//PubmedArticle'):
    pmid = i.xpath(".//PMID")[0]
    lastname = i.xpath(".//Author/LastName")
    lastname = [str(j) for j in lastname]
    firstname = i.xpath(".//Author/ForeName")
    firstname = [str(j) for j in firstname]
    state, country = stateNcountry(i.xpath(".//Affiliation"))
    author_tuples = zip(lastname, firstname, state, country)
    author_list = [list(j) for j in author_tuples]
    for j in author_list:
        j.insert(0, int(pmid))
        author_df.loc[index] = j
        index += 1
    print (author_df)
    return author_df


"""
article_df = pd.DataFrame(columns=('PMID','PubDateYear','PubDateMonth','JournalTitle',
                           'JournalAbbrev','ArticleTitle','AbstractText'))

dfsimple = pd.DataFrame(columns=('PMID','ArticleTitle','AbstractText'))
