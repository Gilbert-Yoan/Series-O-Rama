--Création d'un jeu de données pour le test de la fonction recommandations


------
------SCRIPT UNIQUEMENT ADAPTE A POSTGRESQL
------

--Tables en accord avec le MCD

--Suppression des tables pour repartir d'une base propre
DROP TABLE NOTER CASCADE;
DROP TABLE UTILISATEURS CASCADE;
DROP TABLE SERIES CASCADE;
DROP TABLE MOTS CASCADE;
DROP TABLE CONTENIR CASCADE;

CREATE TABLE SERIES (
    ids INT PRIMARY KEY,
    nomS VARCHAR(50)
);

CREATE TABLE UTILISATEURS (
    idu SERIAL PRIMARY KEY,
    pseudo VARCHAR(30) UNIQUE,
    mail VARCHAR(50) UNIQUE,
    mdp VARCHAR(50),
    isAdmin BOOLEAN
);

CREATE TABLE Noter (
    ids INT,
    idu INT,
    note REAL CHECK (note <= 5.0 AND note >=0),
    CONSTRAINT PK_NOTER PRIMARY KEY(ids, idu),
    CONSTRAINT FK_NOTER_SERIES FOREIGN KEY(ids) REFERENCES SERIES(ids),
    CONSTRAINT FK_NOTER_UTILISATEURS FOREIGN KEY(idu) REFERENCES UTILISATEURS(idu)
);

CREATE TABLE MOTS(
    idm SERIAL PRIMARY KEY,
    mot VARCHAR(45) UNIQUE,
    langue VARCHAR(2),
    CONSTRAINT CK_LANGUE CHECK (langue IN ('FR','EN'))
);

CREATE TABLE CONTENIR(
    idm INT,
    ids INT,
    occurence INT,
    CONSTRAINT PK_CONTENIR PRIMARY KEY (idm,ids),
    CONSTRAINT FK_CONTENIR_SERIES FOREIGN KEY (ids) REFERENCES SERIES,
    CONSTRAINT FK_CONTENIR_MOT FOREIGN KEY (idm) REFERENCES MOTS
);

--Peuplement des tables
--Table SERIES
INSERT INTO SERIES VALUES (1,'Série_Criminelle') ;
INSERT INTO SERIES VALUES (2,'Série_Fantastique') ;
INSERT INTO SERIES VALUES (3,'Série_Enfantine') ;
INSERT INTO SERIES VALUES (4,'Série_Violente') ;

--Table UTILISATEURS
INSERT INTO UTILISATEURS(pseudo,mail,mdp,isAdmin) VALUES('User1','user@gmail.com','123',False) ;
INSERT INTO UTILISATEURS(pseudo,mail,mdp,isAdmin) VALUES('User2','youser@gmail.com','123456',False) ;
INSERT INTO UTILISATEURS(pseudo,mail,mdp,isAdmin) VALUES('Admin1','admin@gmail.com','passroot',True) ;

--Table Mots
INSERT INTO Mots(mot,langue) VALUES ('Corps','FR'),('Monstre','FR'),('Sang','FR'),('Crime','FR'),('Police','FR'),
    ('Pouvoirs','FR'),('Magicien','FR'),('Magie','FR'),('Dragon','FR'), --monstre en commun S1
    ('Princesse','FR'),('Prince','FR'),('Chateau','FR'), --magie & dragon commun avec S2
    ('Armes','FR'),('Meurtre','FR'),('Combat','FR') --sang et police en commun avec S1
;

--Table Contenir
----Le mot d'ID 1 est dans la série d'id 1 260 fois
INSERT INTO CONTENIR VALUES (1,1,260),(2,1,107),(3,1,201),(4,1,148),(5,1,315),
    (6,2,356),(7,2,152),(8,2,211),(9,2,301),(2,2,154),
    (10,3,104),(11,3,111),(12,3,98),(8,3,159),(9,3,132),
    (13,4,221),(14,4,105),(15,4,87),(3,4,247),(5,4,141)
;


--Table NOTER
--UTILISATEURS 1
----Serie 1 est notee par l'UTILISATEURS 1 a 3 etoiles
INSERT INTO NOTER VALUES (1,1,3);
INSERT INTO NOTER VALUES (2,1,2.6);
INSERT INTO NOTER VALUES (4,1,4.5);

--UTILISATEURS 2
INSERT INTO NOTER VALUES (1,2,4);
INSERT INTO NOTER VALUES (2,2,3.5);
INSERT INTO NOTER VALUES (3,2,4);

--UTILISATEURS 3
INSERT INTO NOTER VALUES (2,3,4.5);
INSERT INTO NOTER VALUES (3,3,3.2);
INSERT INTO NOTER VALUES (4,3,2);

COMMIT;

--VERIFICATION DE L'INSERTION DES NOTES PAR LE CALCUL DES MOYENNES
SELECT AVG(note) FROM NOTER WHERE idu=1 ; --attendu 3,36
SELECT AVG(note) FROM NOTER WHERE idu=2 ; --attendu 3,83
SELECT AVG(note) FROM NOTER WHERE idu=3 ; --attendu 3,23






