import nltk
import os
import psycopg2
from nltk.corpus import stopwords


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

"""
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
mypath = "D:\\LP\\ProjetLP\\24"
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
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

#Récupération du nom de toutes les entrées contenues dans le dossier sous-titres (ici on va tester avec un dossier plus petit)
chemin_dossier = 'D:\\LP\\ProjetLP\\sr_test'
noms_series = os.listdir(chemin_dossier)


#Pour chaque série on va
for serie in noms_series :
    #Ouvrir le dossier correspondant
    with os.scandir(chemin_dossier+'\\'+serie) as liste_st :
        #Créer une liste qui va contenir l'ensemble des phrases de la série
        dataset = []
        #Pour chaque fichier de sous-titre
        for fichier in liste_st:
            #ouvrir le ficher
            fileObj = open(chemin_dossier+'\\'+serie+'\\'+fichier.name, "r")
            #stocker les phrases dans un array temporaire (penser à enlever les indications pour placer les sous-titres)
            phrases_fichier = fileObj.read().splitlines()
            #fermer le fichier
            fileObj.close()
            #Supprimer les mots de liaison de la phrase grâce à stopwords
            #Ajouter la phrase dans la liste contenant toutes les phrases de la série
        #Calcul du TF-IDF   
        #Calcul de l'occurence des mots qui selon le TD-IDF sont pertinents pour décrire la série
        #Charger dans la BDD pour cette série l'occurence des mots
    print("fin serie")
print("fin traitement")



            
    



"""
#Récupération des mots de liaison en fonction de la langue 
liaison_mots= stopwords.words('english')

#Définition du dataset
dataset = [
    "I enjoy reading about Machine Learning and Machine Learning is my PhD subject",
    "I would enjoy a walk in the park",
    "I was reading in the library"
]
#TF-IDF 
tfIdfVectorizer=TfidfVectorizer(use_idf=True)
tfIdf = tfIdfVectorizer.fit_transform(dataset)
df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names_out(), columns=["TF-IDF"])
df = df.sort_values('TF-IDF', ascending=False)
print (df.head(25))
"""


