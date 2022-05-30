#Liste imports
import os
from math import *
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import langid
import psycopg2 as pg


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
#https://www.postgresqltutorial.com/postgresql-python/
#Définition méthodes BDD

# Connexion à la base locale PostGreSQL
def connexionBDD ():
    #Création de la connexion
    conn = pg.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="PauliNe1999",
        port = '5432')
    #Création du curseur pour pouvoir manipuler la base
    cur = conn.cursor()
    return conn, cur
		

#https://www.postgresqltutorial.com/postgresql-python/insert/
#Rajout de la serie en BDD et retourne son id 
def insert_serie(connexion, curseur, nom_serie):
    sql = """INSERT INTO serie(noms) VALUES(%s) RETURNING ids;"""
    curseur.execute(sql, (nom_serie,))
    connexion.commit()
    #Renvoi de l'ID de la serie
    return curseur.fetchone()[0]

#Rajout du mot en BDD (s'il n'existe pas déjà)
def insert_mot(connexion, curseur, mot):
    sql = """INSERT INTO mot(mot) VALUES(%s) RETURNING idm;"""
    curseur.execute(sql, (mot,))
    connexion.commit()
    #Renvoi de l'ID du mot
    return curseur.fetchone()[0]


#Rajout de la liaison entre le mot et la serie
def insert_liaison_contenir(connexion, curseur, idMot, idSerie, tfMot):
    sql = """INSERT INTO contenir(idm, ids,occurence) VALUES(%s,%s,%s);"""
    curseur.execute(sql, (idMot,idSerie,tfMot,))
    connexion.commit()


def search_serie(connexion,curseur, serie):
    sql = """SELECT * FROM serie WHERE noms=%s;"""
    curseur.execute(sql, (serie,))
    connexion.commit()

    #Si la serie existe on renvoie son ID, sinon on renvoie None
    res = curseur.fetchone()
    if res is not None:
        return res[0]
    else:
        return None

def search_mot(connexion,curseur, mot):
    sql = """SELECT * FROM mot WHERE mot=%s;"""
    curseur.execute(sql, (mot,))
    connexion.commit()

    #Si le mot existe on renvoie son ID, sinon on renvoie None
    res = curseur.fetchone()
    if res is not None:
        return res[0]
    else:
        return None
    

# Fermeture de la connexion à la base locale PostGreSQL
def fermetureBDD (connexion, curseur):
    curseur.close()
    connexion.close()

#--------------------------------------------------------------------------------
#Début du programme

#Connexion a la BDD
connexion, curseur = connexionBDD()

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

                    #Ajout du fichier propre à la liste (1 fichier => 1 Chaine)
                    liste_temp.append(' '.join(fichier_phrases))


    #print(liste_temp)
    print("Fin traitement serie : "+serie)

    

    #Transformation de la serie en une chaine de caractère  (si la serie contient une version anglaise), calcul du TF et rajout dans la BDD
    if len(liste_temp)>=1 : 
        #print(len(liste_temp))
        serie_propre = (' '.join(liste_temp))

        #Suppression des espaces en trop
        serie_propre = re.sub('\s+', ' ', serie_propre)
        serie_propre = serie_propre.split(' ')
        #print(serie_propre)

        #Rajout de la série en BDD et récupération de l'ID
        #Vérification que la serie n'existe pas déjà
        res_search_serie = search_serie(connexion, curseur,serie)

        #Si la serie n'existe pas on l'insère dans la BDD
        if res_search_serie is None:
            idSerie = insert_serie(connexion, curseur, serie)
        #Si la serie existe on récupère juste son id
        else:
            idSerie=res_search_serie
       

        #Calcul du tf pour les mots de la serie 
        res_tf = calculer_tf(serie_propre)

        for key, value in res_tf[0].items():
            #Vérifier que le mot n'existe pas déjà
            res_search_mot = search_mot(connexion, curseur,key)

            #Si le mot n'existe pas on l'insère dans la BDD
            if res_search_mot is None:
                idMot = insert_mot(connexion, curseur, key)
            #Si le mot existe on récupère juste son id
            else:
                idMot=res_search_mot
           
            #Insertion dans la table Contenir du mot, de la serie et du tf
            insert_liaison_contenir(connexion, curseur, idMot, idSerie, value)


    print('Serie suivante')
#fin for

#Fermeture de l'accès à la BDD
fermetureBDD(connexion, curseur)

 


