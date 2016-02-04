# AcutePainOntology
First Upload

This is a project to develop data for an ontology of acute-pain terms. The goal is to use text from abstracts in PubMed to model frequently published topics related to acute pain. 

To be done:

-Further develop LSI
-word2vec
-comparison of content with chronic pain, acute pain

_______________________________________________________

Ambuj/Nov 12
word2vec model created

demo results


import genism

model_ap = gensim.models.Word2Vec.load("acute_pain_word2vec.mod")
model_ap.most_similar(positive=["adult"])

[('elderly', 0.925835907459259), ('older', 0.9163432121276855), ('often', 0.9131861925125122), ('young', 0.9089071154594421), ('regarded', 0.8877142667770386), ('disabled', 0.8855756521224976), ('female', 0.8775333166122437), ('treated', 0.8761195540428162), ('self-report', 0.8637561202049255), ('forty-eight', 0.8580072522163391)]

Result looks OK for words. We can implement doc2vec model for sentence and abstract level analysis.

_______________________________________________________
  