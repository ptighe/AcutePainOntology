from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import gensim
import sys

d = path.dirname(__file__)
text = ""

#~ Loading word2vec model
model_ap = gensim.models.Word2Vec.load("acute_pain_word2vec.mod")
word_list = model_ap.most_similar(positive=[sys.argv[1]])

#~ Converting output to string
for i in word_list:
    text += (i[0]+ " ")*int(i[1]*1000)

#~ Generating visualization
wc = WordCloud(background_color="white", max_words=50)
wc.generate(text)

#~ Saving output to disk
wc.to_file(path.join(d, "viz.png"))

#~ Show the image
plt.imshow(wc)
plt.axis("off")
plt.show()
