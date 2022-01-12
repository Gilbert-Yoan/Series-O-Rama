import pymongo as mongo
import time
from bson.objectid import ObjectId
from collections import Counter

##Fonction rechercher
##Input : client, type MongoClient, maintient la connexion au serveur Mongo Atlas
##Input : mot, type str, mot à chercher dans les séries
##Output : dictionnaire, type dict, avec une clé d'idObject MongoDB et une valeur du nom de série
def rechercher(client, mot):
    dictionnaire = {}
    ##création d'un dictionnaire id:nom pour les séries correspondantes au mot
    for x in client.petut.series.find({"mots.mot":mot}):  
        dictionnaire[x["_id"]] =  x["serie"]
    return dictionnaire

##Fonction recommander
##Input : client, type MongoClient, maintient la connexion au serveur Mongo Atlas
##Input : recommandations, type liste, liste des ids de séries recommandées
##Input : favoris, type liste, liste des ids des séries mises en favoris
##Input : ignores, type liste, liste des ids des séries ignorées
##Output : series, type dictionnaire, dictionnaire contenant la clé idObject et la valeur nom série
def recommander(client,recommandations,favoris,ignores):
    # récupération des mots des séries
    mots_reco = recuperation_mots(client, recommandations)
    mots_fav= recuperation_mots(client, favoris)
    #addition des Counter rendu par recuperation_mots car les mots sont "souhaitables"
    mots_reco = mots_reco + mots_fav
    mots_ignores = recuperation_mots(client, ignores)
    #soustraction du Counter rendu par recuperation_mots d'ignores pour éliminer les mots non "souhaitables"
    mots_reco = mots_reco - mots_ignores
    #transformation du Counter en dictionnaire
    mots_reco = dict(mots_reco.most_common())
    series = {}
    for mot in mots_reco:
        series.update(rechercher(client,mot))
    return series;

##Fonction recuperation_mots
##Input : client, type MongoClient, maintient la connexion au serveur Mongo Atlas
##Input : liste, type liste, contient des identifiants idObject de MongoDB
##Output : dictionnaire, type Counter, contient les mots et leur nombre d'occurences sur le total des séries dans liste
def recuperation_mots(client, liste):
    dictionnaire = {}
    for i in range (0, len(liste)):
        for x in client.petut.series.find({"_id":liste[i]}):
            mots = x["mots"]
            #mots format : [ { mot : x , occurence : nb }, {...}]
            for k in range(0,len(mots)):
                mot_courrant = mots[k]["mot"]
                if mot_courrant in dictionnaire:
                    dictionnaire[mot_courrant] = dictionnaire[mot_courrant] + mots[k]["occurrence"]
                else:
                    dictionnaire[mot_courrant] = mots[k]["occurrence"]
    return Counter(dictionnaire); 
##connexion à la base de données Mongo ATLAS stockée dans le cloud
client = mongo.MongoClient("mongodb+srv://end:pwd@cluster0.y7gwd.mongodb.net/petut?retryWrites=true&w=majority")


##execution du script et calcul du temps d'execution
#start = time.time()
#res = rechercher(client, "enfant")
#end = time.time()
#print("Temps d'executions de rechercher: ", end-start, " secondes")
#print("Résultat de rechercher: ", res)





##avec vampire en recommandé, macabre en favori et gossip ignoré
recommandations = [ObjectId('61adf89d3195dcef8e2e0a5d')]
favoris  = [ObjectId('61ae00f93195dcef8e2e0a5e')]
ignores = [ObjectId('61ae01ab3195dcef8e2e0a5f')]
##Execution des recommandations et calcul du temps d'execution
start = time.time()
print("Resultat de recommander : ", recommander(client,recommandations,favoris,ignores))
end = time.time()
print("Temps d'execution de recommander : ", end-start)