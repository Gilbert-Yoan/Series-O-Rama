import nltk
import os
import psycopg2
from nltk.corpus import stopwords
stopwords.words('french')

#https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

#https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
def computeIDF(documents):
    import math
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def computeTFIDF(TF, IDF):
    tfidf = {}
    for word, val in TF.items():
        tfidf[word] = val * IDF[word]
    return tfidf

'''
documents = []
for rep in st:
    serie = nom_dossier
    for file in rep:
        with open(file) as read_file:
            documents.append(computeTF(read_file))
dict_idf = computeIDF(documents)
dict_tfidf = computeTFIDF(documents,dict_idf)
'''
"""
docs = [["je m'appelle Yoan et j'aime ça","Je m'appelle Pauline et j'aime ça"],["J'adore les avions","J'apprécie Pauline"]]
documents = []
for rep in docs:
    #serie = nom_dossier
    for file in rep:
        #with open(file) as read_file:
        bagOfWord = file.split(' ')
        wordDict = {}
        uniqueWords = set(bagOfWordsA).union(set(bagOfWordsB))
        for word in bagOfWord:
            if word in wordDict:
                wordDict[word] = wordDict[word] + 1
            else:
                wordDict[word] = 1
        documents.append(computeTF(wordDict,bagOfWord))
print(documents)
dict_idf = computeIDF(documents)
dict_tfidf = computeTFIDF(documents,dict_idf)
print(dict_tfidf)
"""

from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
mypath = "C:\\cygwin64\\home\\djyoy\\st\\24"
onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
documents = [ open(file).read()  for file in onlyfiles ]
#documents = ["je m'appelle Yoan et j'aime ça","Je m'appelle Pauline et j'aime ça","J'adore les avions","J'apprécie Pauline","je m'appelle j'adore les abricots et je suis bien","j'adore les avions je suis libre"]
vect = TfidfVectorizer()
tfidf_matrix = vect.fit_transform(documents)
df = pd.DataFrame(tfidf_matrix.toarray(), columns = vect.get_feature_names_out())
print(df)
cvect = CountVectorizer()
tfidf_matrix = cvect.fit_transform(documents)
df = pd.DataFrame(tfidf_matrix.toarray(), columns = vect.get_feature_names_out())
print(df)
for file in documents:
    os.close(file)