import psycopg2 as pg
import time 
import re

## fonction de recherche des séries correspondantes à un mot fourni
##Fonction rechercher
##Input : connexion, type connection, maintient la connexion au serveur PostGreSQL
##Input : mot, type str, mots à rechercher dans les séries
##Output : series, type liste, contient des tuples au format (idS, nom)
##         avec idS l'identifiant dans la table Serie et nom le nom de la série 
def rechercher(connexion, mots):
    cur = connexion.cursor()
    ##Enlever les espaces en trop
    mots = ' '.join(mots.split())
    ##Découper la chaîne selon les espaces
    mots = re.split(' ', mots)
    expression = "("
    for i in range (0,len(mots)):
        expression = expression+"'"+mots[i]+"'"
        if i == len(mots)-1 :
            expression = expression+")"
        else:
            expression = expression+","

    print(expression)
            
    ##requête permettant de récupérer les ID et noms des séries liées au mot recherché
    SQL = "SELECT s.*, COUNT(s.ids), SUM(c.occurence) FROM SERIE s, CONTENIR c, MOTS m \
        WHERE s.ids = c.ids AND m.idm = c.idm \
        AND m.mot IN {} \
        GROUP BY s.ids ORDER BY COUNT(s.ids) DESC,SUM(c.occurence) DESC;".format(expression)
    cur.execute(SQL)
    #récupération de tous les résultats de la requête 
    series = cur.fetchall()
    return(series) 


## connexion à la base locale PostGreSQL
conn = pg.connect(
    host="localhost",
    database="petut",
    user="postgres",
    password="passroot",
    port = '5432')

## execution du script et calcul du temps d'execution
recherche = str(input("Taper des mots-clés: \n"))
start = time.time()
res = rechercher(conn,recherche)
end = time.time()
print("temps d\'execution de rechercher :", end - start, " secondes")
print("résultats de rechercher: ")
for resultat in res:
    print(resultat)