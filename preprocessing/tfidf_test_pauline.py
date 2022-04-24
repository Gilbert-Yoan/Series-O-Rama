#Liste imports
import os
from math import *
from nltk.corpus import stopwords
import re 

#1 DOCUMENT = 1 SERIE 
#Définiton fonctions nettoyage fichiers

def tester_pattern(pattern, string_test):
    results = re.search(pattern, string_test)
    if results is None:
        return True #pas de match (ne correspond pas au pattern)
    else:
        return False #match

#IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série, le nom du fichier en cours de traitement avec l'extension
#OUT : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série et la langue du fichier
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

    elif os.path.splitext(nom_fichier)[1]==".sub" :
        for phrase in fichier_phrases : 
            fichier_phrases_temp.append(re.sub('^{[0-9]+}{[0-9]+}', '', phrase))

    return fichier_phrases_temp 



# IN  : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série
# OUT : Un array contenant l'ensemble des phrases d'un fichier de sous-titres pour une série sans la ponctuation  
def traitement_mots(fichier_phrases) :
    phrases_temp = []
    #Traitement de la ponctuation
    for phrase in fichier_phrases:
        #Suppression de la ponctuation
        tem_p = re.sub("[^\w\s']", ' ',phrase)
        tem_p = re.sub("[.*']",' ',tem_p)
        #Suppression des espaces en trop (a regarder)
        phrases_temp.append(re.sub('\s+', ' ', tem_p))

    #Passage des mots en minuscule
    for indice in range(len(phrases_temp)):
        phrases_temp[indice] = phrases_temp[indice].lower()

    #Suppression des stop words

    #Lemmatisation des mots 

    #
    return phrases_temp



#--------------------------------------------------------------------------------
#Définition fonctions TFIDF

def calculer_tf(documents):
    tf = []
    df = {}
    sw = stopwords.words('english')
    cur_index = 0
    for document in documents:
        tf.append({})
        for mot in document:
            if mot in tf[cur_index] and mot not in sw:
                tf[cur_index][mot] = tf[cur_index][mot] + 1
            elif mot not in sw:
                tf[cur_index][mot] = 1
                if mot in df:
                    df[mot] += 1
                else:
                    df[mot] = 1
            
        cur_index += 1
    return tf, df


def calculer_idf(documents,df):
    idf = {}
    for mot in df:
        #Ajout de 1 pour éviter le 0
        idf[mot] = 1 + log(len(documents) / df[mot],2)
    return idf

def calculer_tf_idf(tf,idf):
    tfidf = []
    for i in range(0,len(tf)):
        tfidf.append({})
        for mot in tf[i]:
            tfidf[i][mot] = tf[i][mot]*idf[mot]
    return tfidf


#Récupération du nom de toutes les entrées contenues dans le dossier sous-titres (ici on va tester avec un dossier plus petit)
chemin_dossier = 'D:\\LP\\ProjetLP\\sr_test'
noms_series = os.listdir(chemin_dossier)

liste_series = []
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
                fichier_phrases = traitement_mots(fichier_phrases)

            #Ajout du fichier prpore à la serie (1 fichier => 1 Chaine)
            liste_temp.append(' '.join(fichier_phrases))


    #print('LISTE TEMP')
    #print(liste_temp)
    print("Fin serie : "+serie)
    #Transformation de la serie en une chaine de caractère
    liste_series.append(' '.join(liste_temp))

print(liste_series)
i = 0
while i < len(liste_series): 
    liste_series[i] = liste_series[i].split(" ")
    i += 1

#print(liste_series)
print("tf")
print(calculer_tf(liste_series)[0])
print("df")
print(calculer_tf(liste_series)[1])
print("idf")
print(calculer_idf(liste_series,calculer_tf(liste_series)[1]))
print("tf*idf")
print(calculer_tf_idf(calculer_tf(liste_series)[0],calculer_idf(liste_series,calculer_tf(liste_series)[1])))

res_tfidf = calculer_tf_idf(calculer_tf(liste_series)[0],calculer_idf(liste_series,calculer_tf(liste_series)[1]))

#for element in res_tfidf:
    #print (sorted(element,reverse = True))