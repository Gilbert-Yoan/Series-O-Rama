#Liste imports
import os
from math import *
import re 
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import langid


#1 DOCUMENT = 1 SERIE 

#Définition fonction détection de la langue 
# IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série
# OUT : La langue du fichier de sous-titres
def definition_langue_fichier(fichier_phrases):

    #Création d'un dictionnaire pour stocker les résultats de la détection de la langue 
    dict_lg = {'en':0,'oth':0}

    #On récupère seulement une partie des phrases pour tester
    nb_phrases = int(len(fichier_phrases)/3)
    phrases_test = fichier_phrases[0:nb_phrases]

    #Identification de la langue
    for phrase in phrases_test :
        lg = langid.classify(phrase)[0]
        if lg == 'en':
            dict_lg["en"] = dict_lg["en"] + 1
        else:
            dict_lg["oth"] = dict_lg["oth"] + 1

    if dict_lg["en"]>dict_lg["oth"] : 
        return "english"
    else: 
        return "other"


#Définiton fonctions nettoyage fichiers

def tester_pattern(pattern, string_test):
    results = re.search(pattern, string_test)
    if results is None:
        return True #pas de match (ne correspond pas au pattern)
    else:
        return False #match

#IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série, le nom du fichier en cours de traitement avec l'extension
#OUT : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série
def nettoyage_fichier_st (fichier_phrases,nom_fichier):
    fichier_phrases_temp=[]

    #Supprimer les phrases ne contenant que des espaces
    fichier_phrases=[phrase for phrase in fichier_phrases if phrase]

    #Supprimer les indications de placement des sous-titres (pour un fichier srt ou sub)
    if os.path.splitext(nom_fichier)[1]==".srt" :  
        pattern = "^.+-->.+$"
        pattern2 = "^[0-9]+$"

        fichier_phrases_temp=[phrase for phrase in fichier_phrases if tester_pattern(pattern, phrase)]
        fichier_phrases_temp=[phrase for phrase in fichier_phrases_temp if tester_pattern(pattern2, phrase)]

        #Supprimer les indications de formatage du texte
        pattern3 = "^<font color=.*$"
        pattern4 = "^.*<\/font>$"

        fichier_phrases_temp=[phrase for phrase in fichier_phrases_temp if tester_pattern(pattern3, phrase)]
        fichier_phrases_temp=[phrase for phrase in fichier_phrases_temp if tester_pattern(pattern4, phrase)]


    elif os.path.splitext(nom_fichier)[1]==".sub" :
        for phrase in fichier_phrases : 
            fichier_phrases_temp.append(re.sub('^{[0-9]+}{[0-9]+}', '', phrase))

    return fichier_phrases_temp 

# Définition des tags pour pouvoir par la suite faire la lemmatization
#https://www.geeksforgeeks.org/python-lemmatization-approaches-with-examples/
#https://www.holisticseo.digital/python-seo/nltk/lemmatize

def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:         
        return None

# IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série
# OUT : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série sans la ponctuation et avec la lemmatization 
def traitement_mots(fichier_phrases) :
    phrases_temp = []

    #Traitement de la ponctuation
    for phrase in fichier_phrases:
        #Suppression de la ponctuation
        tem_p = re.sub("[^\w\s']", ' ',phrase)
        tem_p = re.sub("[.*']",' ',tem_p)
        phrases_temp.append(re.sub('\s+', ' ', tem_p))

    #Passage des mots en minuscule
    for indice in range(len(phrases_temp)):
        phrases_temp[indice] = phrases_temp[indice].lower()

    
    #Lemmatisation des mots
    lemmatizer = WordNetLemmatizer()
    for indice_phrase in range(len(phrases_temp)):
        #print(phrases_temp[indice_phrase])
        # découpage de la chaine en mots et définition du POS Tag pour chaque mot
        pos_tagged = nltk.pos_tag(nltk.word_tokenize(phrases_temp[indice_phrase])) 
        
        #Transformation des POS Tag de chaque mot en WordNet tag pour la suite
        wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))

        #Lemmatisation de chaque mot, reconstitution en phrase et rajout à la liste
        lemmatized_sentence = []
        for word, tag in wordnet_tagged:
            if tag is None:
                # cas si le tag n'existe pas
                lemmatized_sentence.append(word)
            else:       
                # cas si le tag existe
                lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))

        lemmatized_sentence = " ".join(lemmatized_sentence)

        phrases_temp[indice_phrase] = lemmatized_sentence

    return phrases_temp



#--------------------------------------------------------------------------------
#Définition fonctions TFIDF

def calculer_tf(document):
    #Contient le nombre d'apparitons de chaque terme dans le corpus entier de la serie ({})
    tf = []
    #Contient le nombre de series ou le mot apparait 
    #df = {}
    sw = stopwords.words('english')
    cur_index = 0
    
    tf.append({})
    for mot in document:
        if mot in tf[cur_index] and mot not in sw:
            tf[cur_index][mot] = tf[cur_index][mot] + 1
        elif mot not in sw:
            tf[cur_index][mot] = 1
            #if mot in df:
                #df[mot] += 1
            #else:
                #df[mot] = 1
            
    cur_index += 1
    return tf #, df


def calculer_idf(documents,df):
    idf = {}
    for mot in df:
        idf[mot] = log(len(documents) / df[mot],2)
    return idf

def calculer_tf_idf(tf,idf):
    tfidf = []
    for i in range(0,len(tf)):
        tfidf.append({})
        for mot in tf[i]:
            tfidf[i][mot] = tf[i][mot]*idf[mot]
    return tfidf

#--------------------------------------------------------------------------------
#Début du programme


#Récupération du nom de toutes les entrées contenues dans le dossier sous-titres (ici on va tester avec un dossier plus petit)
chemin_dossier = 'D:\\LP\\ProjetLP\\sr_test'
noms_series = os.listdir(chemin_dossier)

serie_propre = ""
liste_temp = []

#Pour chaque série on va
for serie in noms_series :
    liste_temp= []
    print('Hello serie'+ serie)
    #Ouvrir le dossier correspondant
    with os.scandir(chemin_dossier+'\\'+serie) as liste_fichiers_st :
        #Pour chaque fichier de sous-titre
        for fichier in liste_fichiers_st:
            #ouvrir le ficher
            fileObj = open(chemin_dossier+'\\'+serie+'\\'+fichier.name, "r",encoding='latin-1')
            #stocker les phrases dans un array temporaire
            fichier_phrases = fileObj.read().splitlines()
            #fermer le fichier
            fileObj.close()

            
            #Nettoyer les phrases récupérées du fichier de sous-titre (si il n'est pas vide) en fonction du type de fichier (srt ou sub) et ajout du fichier à la liste temporaire
            if len(fichier_phrases) !=0 :
                fichier_phrases = nettoyage_fichier_st(fichier_phrases,fichier.name)
                if definition_langue_fichier(fichier_phrases)=='english':
                    fichier_phrases = traitement_mots(fichier_phrases)

                    #Ajout du fichier prpore à la serie (1 fichier => 1 Chaine)
                    liste_temp.append(' '.join(fichier_phrases))


    #print('LISTE TEMP')
    #print(liste_temp)
    print("Fin serie : "+serie)

    #Transformation de la serie en une chaine de caractère  (si la serie contient une version anglaise)
    if len(liste_temp)>=1 : 
        print("nb fichiers anglais")
        print(len(liste_temp))
        serie_propre = (' '.join(liste_temp))

    
        #Suppression des espaces en trop
        serie_propre = re.sub('\s+', ' ', serie_propre)
        serie_propre = serie_propre.split(' ')
    
        print(serie_propre)
        #Calcul du tf de la serie 
        res_tf = calculer_tf(serie_propre)

        for serie in res_tf:
            for key, value in serie.items():
                print(key,value)

    print('Serie suivante')
#fin for


#print(liste_series)
#print("tf")
#print(calculer_tf(liste_series))#[0])
#print("df")
#print(calculer_tf(liste_series)[1])
#print("idf")
#print(calculer_idf(liste_series,calculer_tf(liste_series)[1]))
#print("tf*idf")
#print(calculer_tf_idf(calculer_tf(liste_series)[0],calculer_idf(liste_series,calculer_tf(liste_series)[1])))


 #- Si la serie ne possede pas de version anglaise est-ce qu'on l'ajoute dans la BDD ? 
 


