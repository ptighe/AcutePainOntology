
# coding: utf-8
#!/
# In[3]:

# %load topic_model.py


import nltk.data
import numpy as np

import os
import sys
import logging

from Bio import Entrez
from Bio.Entrez import efetch, read

import gensim
from gensim import corpora, models, similarities
from collections import defaultdict


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# In[14]:

def clean_abstract(abstract_data):

    abstract_data = abstract_data.split("\n")
    Flag = False
    parserFlag = False
    abstract_lines = list()

    for lines in abstract_data:
        if "Author information:" in lines:
            Flag = True

        if Flag == True and lines == "":
            parserFlag = True
            Flag = False
            continue

        if Flag == False and lines == "":
            parserFlag = False

        if parserFlag == True:
#             abstract_lines.append(lines.strip().decode('utf-8'))
            abstract_lines.append(lines.strip())

    return " ".join(abstract_lines)


# In[15]:

def fetch_abstract(pmid):
    handle = efetch(db='pubmed', id=pmid, retmode='text', rettype='abstract')
    data = handle.read()
    return data


# In[24]:

def pull_sentences(filename):
    """
        Breaks abstract into sentences
        """
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open(filename)
    data = fp.read()
#     return tokenizer.tokenize(data.decode('utf-8'))
    return tokenizer.tokenize(data)


# In[21]:

def pull_abstracts(keyword, n):
    link_keyword = "+".join(keyword.strip().split(" "))
    exec_string = "curl -vs 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=" + link_keyword + "&retmode=text&retmax=" + str(n) + "' 2>&1 | grep '^<Id>' > pmid.txt"
    os.system(exec_string)

    fileObj = open("pmid.txt", "r")
    idList = list()
    for lines in fileObj:
        idList.append(lines[4:12])

    fq = open("abstracts.txt", "w")
    toolbar_width = len(idList)

    print ("Total PMIDs =", toolbar_width)

    for i, pmid in enumerate(idList):
        p = str((float(i+1)/toolbar_width)*100)[:4]
        sys.stdout.write("\r%s%%" %p)
        sys.stdout.flush()

        abstract_para = clean_abstract(fetch_abstract(pmid))
#         fq.write(abstract_para.encode('utf-8'))
        fq.write(abstract_para)

    print("\n\n")

    fq.close()


# In[22]:

stoplist = ["the", "in", "it", "on", "and", "was", "group", "ci", "of", "to", "that", "a", "were", "by", "il", "to", "this", "is", "for", "has", "been", "are", "with", "or", "an", "had", "has", "be", "they", "them", "as", "at", "we", "there", "from", "who", "not", "=", "no", "methods:", "results:", "than", "all", "vs.", "±", "he", "she", "(p", "but", "their", "our", "but", "also", "can", "conclusions:", "two", "due", "only", "did", "one", "used", "may", "these", "both", "data", "have", "other", "any", "i.t", "1"]

Entrez.email = 'ptighe@gmail.com'


# In[25]:

pull_abstracts("Pain", 50) # first element is the keyword and second element is the maximum number of abstract to be pulled
documents = pull_sentences('abstracts.txt')



# In[29]:

with open("pain_sentences.txt", "w") as fp:
    for i, sentence in enumerate(documents):
        fp.write("%s\n" %sentence)
        documents[i] = sentence
        if documents[i][-1] == ".":
            documents[i] = documents[i][:-1]

texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]
dictionary = corpora.Dictionary(texts)
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()
dictionary.save('pain.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('pain.mm', corpus)
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]


# In[31]:

# LSI model

print("\n\nCreating LSI Model\n\n")
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
corpus_lsi = lsi[corpus_tfidf]

print("\n\n--------------------------------------------------------------------------------------------------------------------------")
print("\n\nLSI Model Details\n\n")
lsi.print_topics(100)
print("--------------------------------------------------------------------------------------------------------------------------\n\n\n")
lsi.save('acutepain_LSImodel.lsi')

# LDA model
print("\n\nCreating LDA Model\n\n")
model = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=5)
print("\n\n--------------------------------------------------------------------------------------------------------------------------")
print("\n\nLDA Model Details\n\n")
model.print_topics(100)
print("--------------------------------------------------------------------------------------------------------------------------")
model.save('acutepain_LDAmodel.lsi')


# In[ ]:
