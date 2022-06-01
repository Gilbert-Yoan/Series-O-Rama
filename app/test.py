#Liste imports python
import os
import sys
import re
import psycopg2 as pg

#Liste des fichiers à importer
curr_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(curr_dir,"BDD","config")
sys.path.append(config_path)
from config import *

# Connexion à la base locale PostGreSQL
def connexionBDD ():
    #Lecture du fichier de configuration
    params = config()
    #Création de la connexion
    conn = pg.connect(**params)
    #Création du curseur pour pouvoir manipuler la base
    cur = conn.cursor()
    return conn, cur
    
def fermetureBDD (connexion, curseur):
    curseur.close()
    connexion.close()
    
    
conn, curs = connexionBDD()
curs.execute("CREATE TABLE test (idt INTEGER PRIMARY KEY, test VARCHAR);")
conn.commit()
fermetureBDD(conn,curs)
