#Liste imports
import os
from math import *
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import psycopg2 as pg
import sys

#Liste des fichiers à importer
curr_dir = os.path.dirname(os.path.abspath(__file__))
python_target = os.path.join(curr_dir,"..","preprocessing")
sys.path.append(python_target)
from methodes_preprocessing import *


#Ici on suppose que les search_words sont des chaines de caractères simples séparées par des espaces
def get_search_results(cursor, search_words):
    words_list = search_words.split(' ')
    print(words_list)
    res = []
    for word in words_list:
        query = "WITH allDoc AS (SELECT COUNT(s.ids) total FROM serie s) , \
                word_DF AS (SELECT COUNT(s.ids) as df FROM serie s, contenir c, mot m WHERE m.idm = c.idm AND s.ids = c.ids AND m.mot = %s), \
                word_doc AS (SELECT c.occurence curr_occ, m.mot mot, s.ids serie_id, s.noms nom FROM serie s, contenir c, mot m \
                        WHERE m.idm = c.idm AND s.ids = c.ids AND m.mot = %s) \
                SELECT serie_id, nom, mot,curr_occ tf,df, LOG(2.0, total/df) idf, curr_occ*LOG(2.0, total/df) as tfidf FROM word_df, allDoc, word_doc;"

        cursor.execute(query, (word, word))
        res.append(cursor.fetchall())
    return res



#-----------------------------------------------------------------------------
#https://www.postgresqltutorial.com/postgresql-python/
#Définition méthodes BDD

# Connexion à la base locale PostGreSQL
def connexionBDD ():
    #Création de la connexion
    conn = pg.connect(
        host="localhost",
        database="petut",
        user="postgres",
        password="passroot",
        port = '5432')
    #Création du curseur pour pouvoir manipuler la base
    cur = conn.cursor()
    return conn, cur
		
# Fermeture de la connexion à la base locale PostGreSQL
def fermetureBDD (connexion, curseur):
    curseur.close()
    connexion.close()

#--------------------------------------------------------------------------------
#Début du programme

#Connexion a la BDD
connexion, curseur = connexionBDD()

res = get_search_results(curseur, "Magie Crime")
    
print(res)
#Fermeture de l'accès à la BDD
fermetureBDD(connexion, curseur)
