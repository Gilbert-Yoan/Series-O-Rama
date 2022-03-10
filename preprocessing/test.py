import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer 
import os

# this is a very toy example, do not try this at home unless you want to understand the usage differences 
docs=["the house had a tiny little mouse", 
"the cat saw the mouse", 
"the mouse ran away from the house", 
"the cat finally ate the mouse", 
"the end of the mouse story"
]


#Récupération du nom de toutes les entrées contenues dans le dossier sous-titres (ici on va tester avec un dossier plus petit)
chemin_dossier = 'D:\\LP\\ProjetLP\\sr_test'
noms_series = os.listdir(chemin_dossier)
nb_series = 0

#Créer deux dataset (un pour chaque langue), chacun de ses dataset contenant des chaines de caractères (chaque chaine représentant une série)
dataset_vf = {}
dataset_vo = {}

#Créer un dataset qui contient un dataset pour l'angais et un autre pour le françcais 
dataset = []


fileObj = open("D:/LP/ProjetLP/Series-O-Rama/preprocessing/notes_Pauline _ChargementBDD/StopwFrench.txt", "r")
#stocker les phrases dans un array temporaire
stop_w_french = fileObj.read().splitlines()
liste_stop_w = stop_w_french
fileObj.close()

#Pour chaque série on va
for serie in noms_series :
    nb_series = nb_series +1
    #Créer les dataset temporaires pour une série pour permettre l'ajout plus tard dans les dataset définitfs (ici une chaine représente 1 fichier de sous-titres)
    dataset_vo_temp = []
    dataset_vf_temp = []

    #Créer l'entrée pour la série dans les deux dictionaires
    if serie not in dataset_vf.keys() : 
        dataset_vf[serie] = ""
    if serie not in dataset_vo.keys() :
        dataset_vo[serie] = ""

    #Ouvrir le dossier correspondant
    with os.scandir(chemin_dossier+'\\'+serie) as liste_fichiers_st :
        #Pour chaque fichier de sous-titre
        for fichier in liste_fichiers_st:
            #ouvrir le ficher
            fileObj = open(chemin_dossier+'\\'+serie+'\\'+fichier.name, "r",encoding='latin-1')
            #stocker les phrases dans un array temporaire
            fichier_phrases = fileObj.read().splitlines()
            phrases_propres = []
            for phrase in fichier_phrases:
                if not phrase[:10].isalnum():
                    fichier_phrases.remove(phrase)
                else:
                    
                    phrase_tmp = [mot for mot in phrase.lower().split() if mot not in liste_stop_w and not mot.isdigit()]
                    phrases = ' '.join(phrase_tmp)
                    phrases_propres.append(phrases)


            #fermer le fichier
            fileObj.close()

            #Nettoyer les phrases récupérées du fichier de sous-titre (si il n'est pas vide) en fonction du type de fichier (srt ou sub) et ajout du fichier au dataset correspondant
            if len(fichier_phrases) !=0 :
                dataset_vf_temp.append(' '.join(phrases_propres))

    print("Fin serie : "+serie)

    # Rajout de la serie au dataset correspondant
    dataset_vf[serie] = ' '.join(dataset_vf_temp)

    
#Ajout des deux dataset au dataset final (vérifier avant l'ajout si le dataset existe)
dataset.append(str(dataset_vf.values()))

# settings that you use for count vectorizer will go here 
tfidf_vectorizer=TfidfVectorizer(use_idf=True) 
# just send in all your docs here 
tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(dataset)
#print(dataset)
#print(tfidf_vectorizer_vectors)
# get the first vector out (for the first document) 
first_vector_tfidfvectorizer=tfidf_vectorizer_vectors[0] 
# place tf-idf values in a pandas data frame 
df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=[noms_series[0]])
df = df.sort_values(by=[noms_series[0]],ascending=False)
print(df.to_string())