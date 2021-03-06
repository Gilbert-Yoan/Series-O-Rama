#Liste imports
import os
import psycopg2 as pg
import json
import sys
import unicodedata
import string

#Liste des fichiers à importer
curr_dir = os.path.dirname(os.path.abspath(__file__))
python_target = os.path.join(curr_dir,"..","preprocessing")
sys.path.append(python_target)

from methodes_preprocessing import traitement_mots, connexionBDD, fermetureBDD
 

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.printable).lower()


#Ici on suppose que les search_words sont des chaines de caractères simples séparées par des espaces
def get_search_results(cursor, search_words):
    words_list = search_words.split(' ')

    #Récupération du dictionnaire FR-EN JSON
    with open(os.path.join(curr_dir,'fr-en-dict.json'),'r',encoding='utf8') as json_file:
        dictionnaire = json.load(json_file)

    #Traduction approximative des mots tapés en Français
    words_list_en = []
    for word in words_list:
        try:
            for w in dictionnaire[remove_accents(word)] :
                words_list_en.append(w)
        except KeyError:
            words_list_en.append(word)

    #print(word_list_en) pour afficher les traductions réalisés par le dictionnaire
    res = traitement_mots(words_list_en)
    #print(res) pour afficher les résultats lemmatizés
    res = []
    for word in words_list_en:
        #print(word)
        query = "WITH allDoc AS (SELECT COUNT(s.ids) total FROM serie s) , \
                word_DF AS (SELECT COUNT(s.ids) as df FROM serie s, contenir c, mot m WHERE m.idm = c.idm AND s.ids = c.ids AND LOWER(m.mot) = LOWER(%s)), \
                word_doc AS (SELECT c.occurence curr_occ, m.mot mot, s.ids serie_id, s.noms nom FROM serie s, contenir c, mot m \
                        WHERE m.idm = c.idm AND s.ids = c.ids AND LOWER(m.mot) = LOWER(%s)) \
                SELECT serie_id, nom, curr_occ*LOG(2.0, total/df) as tfidf FROM word_df, allDoc, word_doc ORDER BY tfidf DESC;"

        cursor.execute(query, (word, word))
        res.append(cursor.fetchall())

    #print(res)

    res_str = ""
    for r in res:
        for tup in r:
            query = "SELECT CASE WHEN EXISTS (SELECT note from noter where ids=%s) THEN AVG(note) ELSE 0 END FROM noter WHERE ids=%s;"
            cursor.execute(query, (tup[0],tup[0]))
            note = cursor.fetchall()
            res_str = res_str +str(tup[0]) + "~" + tup[1] + "~" + str(note[0][0]) +";" 

    return res_str[:-1]


#--------------------------------------------------------------------------------
#Début du programme

#Connexion a la BDD
connexion, curseur = connexionBDD()

#Test français anglais pour traduction
res = get_search_results(curseur, sys.argv[1])
    
print(res)
#Fermeture de l'accès à la BDD
fermetureBDD(connexion, curseur)
