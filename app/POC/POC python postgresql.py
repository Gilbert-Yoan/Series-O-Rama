import psycopg2 as pg
import time 

## fonction de recherche des séries correspondantes à un mot fourni
##Fonction rechercher
##Input : connexion, type connection, maintient la connexion au serveur PostGreSQL
##Input : mot, type str, mot à rechercher dans les séries
##Output : series, type liste, contient des tuples au format (idS, nom)
##         avec idS l'identifiant dans la table Serie et nom le nom de la série 
def rechercher(connexion, mot):
    cur = connexion.cursor()
    ##requête permettant de récupérer les ID et noms des séries liées au mot recherché
    SQL = 'SELECT serie.idS, serie.serie FROM serie, liaison, mot \
    WHERE serie.idS = liaison.idS AND mot.idM = liaison.idM AND mot=\'{}\' \
    ORDER BY occurence DESC ;'.format(mot)
    cur.execute(SQL)
    #récupération de tous les résultats de la requête 
    series = cur.fetchall()
    return(series) 

##Fonction recommander
##Input : connexion, type connection, maintient la connexion au serveur PostGreSQL
##Input : recommandations, type liste, contient les identifiants des séries recommandées dans la table Série
##Input : favoris, type liste, contient les identifiants des séries mises en favoris dans la table Série
##Input : ignores, type liste, contient les identifiants des séries ignorées dans la table Série
##Output : series, type liste, contient une liste de tuple au format (id, nom)
##          avec id l'id dans la table Série de PostGreSQL et nom le nom de la série dans cette même table
def recommander(connexion, recommandations, favoris, ignores):
    cur = connexion.cursor()
    ##sont acceptable les séries recommandées et favoris uniquement
    acceptable = []
    acceptable[:0] = recommandations
    acceptable[:0] = favoris  
    acceptable = list(set(acceptable) - set(ignores))
    acceptable = "('" + "', '".join(str(x) for x in acceptable) + "')"
    ##requête permettant de récupérer les mots et le nombre d'occurence
    SQL = 'SELECT mot, SUM(occurence) FROM liaison, mot \
    WHERE liaison.idS in {} and liaison.idM = mot.idM GROUP BY mot ORDER BY SUM(occurence) DESC ;'.format(acceptable)
    cur.execute(SQL)
    mots = cur.fetchall()
    series = []
    for mot in mots:
        series[:0] = rechercher(connexion,mot[0])
    series = list(set(series))
    return(series)

## connexion à la base locale PostGreSQL
conn = pg.connect(
    host="localhost",
    database="petut",
    user="postgres",
    password="passroot",
    port = '5432')

## execution du script et calcul du temps d'execution
start = time.time()
res = rechercher(conn,"enfant")
end = time.time()
print("temps d\'execution de rechercher :", end - start, " secondes")
print("résultat de rechercher", res)


## execution du script et calcul du temps d'execution
##avec vampire en recommandé, macabre en favori et gossip ignoré
start = time.time()
res = recommander(conn,[1],[2],[3])
end = time.time()
print("temps d\'execution de recommander : ", end-start , " secondes")
print("resultat de recommander : ", res)