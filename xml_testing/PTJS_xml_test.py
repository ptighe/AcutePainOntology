
# coding: utf-8

# In[48]:

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from lxml import objectify
import pandas as pd
import os


# In[49]:

os.getcwd()
# os.chdir('xml_testing')


# In[50]:

path='pubmed_result_tighe.xml'
tree = objectify.parse(open(path))


# In[ ]:

def stateNcountry(affilation):    
    state = []
    country = []
    city=[]
    for i in affilation:
        words = str(i).split(" ")
        if '@' in words[-1]:
            words.pop()
        if len(words) >= 2:
            country.append(words.pop().rstrip('.').rstrip(',').rstrip(':').rstrip(';'))
            state.append(words.pop().rstrip('.').rstrip(',').rstrip(':').rstrip(';'))
            city.append(words.pop().rstrip('.').rstrip(',').rstrip(':').rstrip(';'))
    return city,state,country


# In[ ]:

author_df = pd.DataFrame(columns=('PMID','LastName','FirstName','City','State', 'Country'))
index = 0


# In[ ]:

for i in tree.xpath('//PubmedArticle'):
    pmid = i.xpath(".//PMID")[0]
    lastname = i.xpath(".//Author/LastName")
    lastname = [str(j) for j in lastname]
    firstname = i.xpath(".//Author/ForeName")
    firstname = [str(j) for j in firstname]
    city, state, country = stateNcountry(i.xpath(".//Affiliation"))
    author_tuples = zip(lastname, firstname, city, state, country)
    author_list = [list(j) for j in author_tuples]
    for j in author_list:
        j.insert(0, int(pmid))
        author_df.loc[index] = j
        index += 1
#     return author_df


# In[ ]:

for i in tree.xpath('//PubmedArticle'):
    pmid = i.xpath(".//PMID")[0]
    lastname = i.xpath(".//Author/LastName")
    lastname = [str(j) for j in lastname]
    firstname = i.xpath(".//Author/ForeName")
    firstname = [str(j) for j in firstname]
    city, state, country = stateNcountry(i.xpath(".//Affiliation"))
    author_tuples = zip(lastname, firstname, city, state, country)
    author_list = [list(j) for j in author_tuples]


# In[104]:

article_df = pd.DataFrame(columns=('PMID','JournalTitle','ArticleTitle','AbstractText'))
index = 0


# In[105]:

for i in tree.xpath('//PubmedArticle'):
    pmid = i.xpath(".//PMID")[0]
    journaltitle = i.xpath('.//Article/Journal/Title/text()')
    articletitle = i.xpath(".//Article/ArticleTitle/text()")
    abstracttext = i.xpath('.//AbstractText')
    ab_tuples = zip(journaltitle, articletitle,abstracttext)
    ab_list = [list(j) for j in ab_tuples]
    for j in ab_list:
        j.insert(0,int(pmid))
        article_df.loc[index] = j
        index += 1


# In[106]:

article_df.loc[i,'AbstractText']


# In[103]:

del(article_df)


# In[ ]:



