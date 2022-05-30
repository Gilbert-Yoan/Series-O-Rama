import psycopg2 as pg
import time 

##Fonction recommander
##Input : connexion, type connection, maintient la connexion au serveur PostGreSQL
##Input : user, type entier, ID de l'utilisateur 
##Input : serie, type entier, ID de la série dont la note est à estimer

def recommander(connexion, user,serie):
    cur = connexion.cursor()
    ##requête permettant de récupérer la note de l'utilisateur
    SQL = "WITH MOYENNES AS (SELECT idu, AVG(note) AS moy FROM NOTER GROUP BY idu),\
        \
        NOTES_RETRANCHES AS ( \
            SELECT m.idu,n.ids, note-moy AS note FROM NOTER n, MOYENNES m \
            WHERE m.idu IN (SELECT idu FROM NOTER WHERE ids IN (SELECT ids FROM NOTER WHERE idu={})) \
            AND m.idu = n.idu), \
        HAUT_SIMILARITES AS ( \
            SELECT SUM(n.note*n2.note)as somme,n.idu \
            FROM NOTES_RETRANCHES n, NOTES_RETRANCHES n2 \
            WHERE n.idu!=n2.idu AND n2.idu={} AND n.ids=n2.ids \
            GROUP BY n.idu),\
        BAS_SIMILARITES AS ( \
            SELECT SQRT(SUM(POWER(n.note,2))*SUM(POWER(n2.note,2))) as racine, n.idu \
            FROM NOTES_RETRANCHES n, NOTES_RETRANCHES n2 \
            WHERE n.idu!=n2.idu AND n2.idu={} AND n.ids=n2.ids \
            GROUP BY n.idu), \
        SIMILARITES AS (SELECT somme/racine as similarite, h.idu FROM HAUT_SIMILARITES h,BAS_SIMILARITES b WHERE h.idu=b.idu), \
        PARTIE_HAUTE AS (SELECT SUM(n.note*s.similarite) as haute FROM NOTES_RETRANCHES n, SIMILARITES s WHERE n.idu = s.idu AND n.ids = {}),\
        SOMME_SIMILARITES AS (SELECT SUM(ABS(similarite)) as sim FROM SIMILARITES) \
	    SELECT moy+(haute/sim) FROM MOYENNES m, PARTIE_HAUTE p, SOMME_SIMILARITES s WHERE m.idu = {};".format(user,user,user,serie,user)
    cur.execute(SQL)
    #récupération de tous les résultats de la requête 
    series = cur.fetchone()
    return(series) 















## connexion à la base locale PostGreSQL
conn = pg.connect(
    host="localhost",
    database="petut",
    user="postgres",
    password="passroot",
    port = '5432')

## execution du script et calcul du temps d'execution
user = int(input("Taper le numéro d'utilisateur: \n"))
serie = int(input("Taper l'ID de la série: \n"))
start = time.time()
#utilisateur 3 , deviner la note de la série 1
res = recommander(conn,user,serie)
end = time.time()
print("temps d\'execution de la prédiction :", end - start, " secondes")
print("Note estimée pour l'utilisateur: ",res[0])