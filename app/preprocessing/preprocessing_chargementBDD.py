import sys

#Liste des fichiers à importer
sys.path.append( 'D:\LP\ProjetLP\Series-O-Rama\preprocessing')
from methodes_preprocessing import *


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

    #Transformation de la serie en une chaine de caractère  (si la serie contient une version anglaise), calcul du TF et rajout dans la BDD
    if len(liste_temp)>=1 : 
        serie_propre = (' '.join(liste_temp))

        #Suppression des espaces en trop
        serie_propre = re.sub('\s+', ' ', serie_propre)
        serie_propre = serie_propre.split(' ')
        

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
#fin for




#Fermeture de l'accès à la BDD
fermetureBDD(connexion, curseur)

 


