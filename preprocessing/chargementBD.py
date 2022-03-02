from unittest.case import DIFF_OMITTED
import nltk
import os
import psycopg2
from nltk.corpus import stopwords
import re
import string 
import langid # pip install langid==1.1.6


#Début déclaration méthodes

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


def tester_pattern(pattern, string_test):
    results = re.search(pattern, string_test)
    if results is None:
        return True #pas de match (ne correspond pas au pattern)
    else:
        return False #match


# IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série
# OUT : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série sans la ponctuation  
def traitement_ponctuation(fichier_phrases) :
    phrases_temp = []
    for phrase in fichier_phrases:
        #Suppression de la ponctuation
        tem_p = re.sub("[^\w\s']", ' ',phrase)
        #Suppression des espaces en trop
        phrases_temp.append(re.sub('\s+', ' ', tem_p))
    return phrases_temp


# IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série
# OUT : La langue du fichier de sous-titres
def definition_langue_fichier(fichier_phrases):

    #Création d'un dictionnaire pour stocker les résultats de la détection de la langue 
    dict_lg = {'en':0,'fr':0}

    #On récupère seulement une partie des phrases pour tester
    nb_phrases = int(len(fichier_phrases)/3)
    phrases_test = fichier_phrases[0:nb_phrases]

    #Identification de la langue
    for phrase in phrases_test :
        lg = langid.classify(phrase)[0]
        if lg == 'en':
            dict_lg["en"] = dict_lg["en"] + 1
        elif lg =='fr':
            dict_lg["fr"] = dict_lg["fr"] + 1
    
    if dict_lg["en"]>dict_lg["fr"] : 
        return "english"
    else: 
        return "french"


# IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série avec des phrases sans indications de sous-titres et de ponctuation
# OUT : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série sans les mots de liaison
def traitement_stop_words(fichier_phrases) :

    #Détection de la langue du fichier de sous-titres que l'on traite
    langue  = definition_langue_fichier(fichier_phrases)
    liste_stop_w = stopwords.words(langue)
   
    fichier_phrases_temp = []
    #Suppression des mots de liaison
    for phrase in fichier_phrases :
        temp_phrase = [mot for mot in phrase.lower().split() if mot not in liste_stop_w]
        #Re-création de la phrase en une chaine
        temp_phrase = ' '.join(temp_phrase)
        #Ajout au tableau
        fichier_phrases_temp.append(temp_phrase)

    return fichier_phrases_temp


#IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série, le nom du fichier en cours de traitement avec l'extension
#OUT : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série
def nettoyage_fichier_st (fichier_phrases,nom_fichier):

    fichier_phrases_temp=[]
    fichier_propre=[]

    #Supprimer les phrases ne contenant que des espaces
    fichier_phrases=[phrase for phrase in fichier_phrases if phrase]

    #Supprimer les indications de placement des sous-titres (pour un fichier srt ou sub)
    if os.path.splitext(nom_fichier)[1]==".srt" :  
        pattern = "^.+-->.+$"
        pattern2 = "^[0-9]+$"

        fichier_phrases_temp=[phrase for phrase in fichier_phrases if tester_pattern(pattern, phrase)]
        fichier_phrases_temp=[phrase for phrase in fichier_phrases_temp if tester_pattern(pattern2, phrase)]

    elif os.path.splitext(nom_fichier)[1]==".sub" :
        for phrase in fichier_phrases : 
            fichier_phrases_temp.append(re.sub('^{[0-9]+}{[0-9]+}', '', phrase))
            
    fichier_phrases_temp = traitement_ponctuation(fichier_phrases_temp)
    fichier_phrases_temp = traitement_stop_words(fichier_phrases_temp)

    fichier_propre = fichier_phrases_temp

    return fichier_propre 



#Fin déclaration méthodes 
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
nb_series = 0

#Pour chaque série on va
for serie in noms_series :
    nb_series = nb_series +1
    #Ouvrir le dossier correspondant
    with os.scandir(chemin_dossier+'\\'+serie) as liste_fichiers_st :
        #Créer une liste qui va pour une serie, contenir pour chaque fichier de st les phrases nettoyés [['phrase1,phrase2'],['phrase1,phrase2']] (1 dataset par série)
        dataset = []
        #Pour chaque fichier de sous-titre
        for fichier in liste_fichiers_st:
            #ouvrir le ficher
            fileObj = open(chemin_dossier+'\\'+serie+'\\'+fichier.name, "r",encoding='ansi')
            #stocker les phrases dans un array temporaire
            fichier_phrases = fileObj.read().splitlines()
            #fermer le fichier
            fileObj.close()

            #Nettoyer les phrases récupérées du fichier de sous-titre (si il n'est pas vide) en fonction du type de fichier (srt ou sub) et ajout du fichier au dataset
            if len(fichier_phrases) !=0 :
                fichier_ok = nettoyage_fichier_st(fichier_phrases,fichier.name)
                dataset.append(fichier_ok)
                #Affichage pour vérifier le résultat de chaque fichier (1 fichier = 1 array)
                print(fichier_ok)
                print("---------------------")
            
    print(len(dataset))
    print("Fin serie : "+serie)
    #print(dataset)
    
    #Calcul du TF-IDF sur le dataset 
        #Calcul de l'occurence des mots qui selon le TD-IDF sont pertinents pour décrire la série
        #Chargement dans la BDD
            #Table Serie
            #Table Mot
            #Table Contenir
print("fin traitement")
print(nb_series)