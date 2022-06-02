import psycopg2 as pg
import os
import sys
#Liste des fichiers à importer
curr_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(curr_dir,"config")
sys.path.append(config_path)
from config import *

#Imports des commandes connexion et fermeture BDD
functions_path = os.path.join(curr_dir,"..","..","preprocessing")
sys.path.append(functions_path)
print(functions_path)
from methodes_preprocessing import connexionBDD, fermetureBDD

query = "\
DROP TABLE IF EXISTS NOTER CASCADE; \
DROP TABLE IF EXISTS UTILISATEUR CASCADE; \
DROP TABLE IF EXISTS SERIE CASCADE; \
DROP TABLE IF EXISTS MOT CASCADE; \
DROP TABLE IF EXISTS CONTENIR CASCADE; \
DROP TABLE IF EXISTS CHERCHER CASCADE; \
 \
CREATE TABLE SERIE ( \
    ids SERIAL PRIMARY KEY, \
    nomS VARCHAR(50) UNIQUE \
); \
 \
CREATE TABLE UTILISATEUR ( \
    idu SERIAL PRIMARY KEY, \
    pseudo VARCHAR(30) UNIQUE, \
    mail VARCHAR(50) UNIQUE, \
    mdp VARCHAR(50), \
    isAdmin BOOLEAN \
); \
 \
CREATE TABLE NOTER ( \
    ids INT, \
    idu INT, \
    note REAL CHECK (note <= 5.0 AND note >=0), \
    CONSTRAINT PK_NOTER PRIMARY KEY(ids, idu), \
    CONSTRAINT FK_NOTER_serie FOREIGN KEY(ids) REFERENCES serie(ids), \
    CONSTRAINT FK_NOTER_utilisateur FOREIGN KEY(idu) REFERENCES utilisateur(idu) \
); \
 \
CREATE TABLE MOT( \
    idm SERIAL PRIMARY KEY, \
    mot VARCHAR(100), \
    CONSTRAINT UNIQUE_MOT UNIQUE (mot) \
); \
 \
CREATE TABLE CONTENIR( \
    idm INT, \
    ids INT, \
    occurence INT, \
    CONSTRAINT PK_CONTENIR PRIMARY KEY (idm,ids), \
    CONSTRAINT FK_CONTENIR_serie FOREIGN KEY (ids) REFERENCES serie, \
    CONSTRAINT FK_CONTENIR_MOT FOREIGN KEY (idm) REFERENCES mot \
); \
 \
CREATE TABLE CHERCHER( \
    idu INT, \
    idm INT, \
    date_rech TIMESTAMP default current_timestamp, \
    CONSTRAINT PK_CHERCHER PRIMARY KEY (idu,idm), \
    CONSTRAINT FK_CHERCHER_UTILISATEUR FOREIGN KEY (idu) REFERENCES utilisateur, \
    CONSTRAINT FK_CHERCHER_mot FOREIGN KEY (idm) REFERENCES mot \
);"

#print(query)
connexion, curseur = connexionBDD()
curseur.execute(query)
connexion.commit()

query_default_user = "INSERT INTO utilisateur VALUES (1,'user_default',null,null,False);"
curseur.execute(query_default_user)
connexion.commit()

query_function = "CREATE OR REPLACE FUNCTION defNote() RETURNS TRIGGER\
    AS $$ BEGIN INSERT INTO noter(idu,ids,note) VALUES (1, new.ids, 0); RETURN NEW; END; $$ LANGUAGE plpgsql;"

query_trigger = "CREATE TRIGGER triggerDefNotes AFTER INSERT ON SERIE FOR EACH ROW\
    EXECUTE PROCEDURE defNote();"
curseur.execute(query_trigger)
connexion.commit()

fermetureBDD(connexion,curseur)
