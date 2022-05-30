import psycopg2 as pg

##Fonctions peuplement BDD

##Peuplement de la table serie
def peupler_SERIE(cursor, serie):
    query = "SELECT ids FROM SERIE where nomS = %s"
    cursor.execute(query,(serie,))
    series = cursor.fetchall()
    if len(series) == 0:
        query = "INSERT INTO SERIE (nomS) VALUES (%s)"
        cursor.execute(query,(serie,))
        return 0
    return 1

##Peuplement de la table MOT
def peupler_MOT(cursor, lg, word_arr):
    for word in word_arr:
        #On vérifie que le mot dans cette langue n'existe pas
        query = "SELECT idm from MOT where mot = %s and langue=%s"
        cursor.execute(query,(word,lg))
        mot = cursor.fetchall()
        #S'il n'existe pas, on l'ajoute
        if len(mot) == 0:
            query = "INSERT INTO MOT (mot,langue) VALUES (%s,%s)"
            cursor.execute(query,(word,lg))


##Peuplement de la table CONTENIR
def peupler_CONTENIR(cursor,word_arr,lg,count_arr,serie):
    for i in range(0,len(word_arr)):
        #On récupère la série concernée
        query = "SELECT ids FROM SERIE WHERE nomS = %s"
        cursor.execute(query,(serie,))
        idS = cursor.fetchall()[0][1]

        #On récupère le mot courrant
        query = "SELECT idm FROM MOT WHERE mot = %s and langue = %s"
        cursor.execute(query,(word_arr[i],lg))
        idM = cursor.fetchall()[0][1]

        #On peuple contenir
        query = "INSERT INTO CONTENIR VALUES (%s,%s,%s)"
        cursor.execute(query,(idM,idS,count_arr[i]))


#array format :
# [serie, langue, mots1, occ1, ... , motn, occn]
def peupler(array):
    connexion = pg.connect(
    host="localhost",
    database="petut",
    user="postgres",
    password="passroot",
    port = '5432')

    cur = connexion.cursor()

    #Récupération des informations de la liste envoyée
    serie = array[0]
    langue = array[1]
    array_word_count = array[2:]
    word = array_word_count[0::2]
    count = array_word_count[1::2]
    
    valide = peupler_SERIE(cur,serie)
    if not valide:
        peupler_MOT(cur,langue,word)
        peupler_CONTENIR(cur,word,langue,count,serie)
        cur.close()
        return valide
    cur.close()
    return valide
