--Création d'un jeu de données pour le test de la fonction recommandations

--Tables en accord avec le MCD

--Suppression des tables pour repartir d'une base propre
DROP TABLE Aimer CASCADE CONSTRAINTS ;
DROP TABLE Utilisateur CASCADE CONSTRAINTS ;
DROP TABLE Serie CASCADE CONSTRAINTS ;

CREATE TABLE Serie (
    ids INT PRIMARY KEY,
    serie VARCHAR(50)
);

CREATE TABLE Utilisateur (
    idu INT PRIMARY KEY,
    mail VARCHAR(50),
    mdp VARCHAR(50)
);

CREATE TABLE Aimer (
    ids INT,
    idu INT,
    note NUMBER,
    CONSTRAINT PK_AIMER PRIMARY KEY(ids, idu),
    CONSTRAINT FK_AIMER_SERIE FOREIGN KEY(ids) REFERENCES Serie(ids),
    CONSTRAINT FK_AIMER_UTILISATEUR FOREIGN KEY(idu) REFERENCES Utilisateur(idu)
);

--Peuplement des tables
--Table Serie
INSERT INTO Serie VALUES (1,'SérieA') ;
INSERT INTO Serie VALUES (2,'SérieB') ;
INSERT INTO Serie VALUES (3,'SérieC') ;
INSERT INTO Serie VALUES (4,'SérieD') ;

--Table Utilisateur
INSERT INTO Utilisateur(idu) VALUES(1) ;
INSERT INTO Utilisateur(idu) VALUES(2) ;
INSERT INTO Utilisateur(idu) VALUES(3) ;


--Table Aimer
--Utilisateur 1
INSERT INTO Aimer VALUES (1,1,3);
INSERT INTO Aimer VALUES (2,1,2.6);
INSERT INTO Aimer VALUES (4,1,4.5);

--Utilisateur 2
INSERT INTO Aimer VALUES (1,2,4);
INSERT INTO Aimer VALUES (2,2,3.5);
INSERT INTO Aimer VALUES (3,2,4);

--Utilisateur 3
INSERT INTO Aimer VALUES (2,3,4.5);
INSERT INTO Aimer VALUES (3,3,3.2);
INSERT INTO Aimer VALUES (4,3,2);

--VERIFICATION DE L'INSERTION DES NOTES PAR LE CALCUL DES MOYENNES
SELECT AVG(note) FROM Aimer WHERE idu=1 ; --attendu 3,36
SELECT AVG(note) FROM Aimer WHERE idu=2 ; --attendu 3,83
SELECT AVG(note) FROM Aimer WHERE idu=3 ; --attendu 3,23



---------------------------------DEBUT DE LA RECOMMANDATION POUR UN UTILISATEUR PRECIS---------------------------------------------------
--Récupérer uniquement les séries que l'utilisateur (ici le 3) n'a pas encore notéeS (donc pas vue)
SELECT ids 
FROM Serie 

MINUS

SELECT ids
FROM Aimer
WHERE idu='&id_user' ; --attendu 1


--Pour chaque série non notée par l'utilisateur N (ici 3) on va calculer la note qu'il pourrait donner
--en fonction des notes déjà données pour cette série par d'autres utilisateurs par rapport aux séries en commun avec l'utilisateur 3
--On devra ensuite décider en fonction de la note prédite si on propose ou non la série

--PARTIE 1 - RECUPERER LES UTILISATEURS (QUI ONT VUE LA SERIE 1 ET QUI ONT DES SERIES EN COMMUN AVEC L'UTILISATEUR 3) 
SELECT idu
FROM Aimer
WHERE ids IN (SELECT ids FROM Aimer WHERE ); 


--PARTIE 2 - POUR CHAQUE UTILISATEUR
    --PARTIE 2.1 - CALCUL DE LA MOYENNE DES NOTES
    --PARTIE 2.2 - ON RETRANCHE A CHAQUE NOTE DE SERIE LA MOYENNE (A STOCKER ?)
    --PARTIE 2.3 - CALCUL DE LA SIMILARITE (A STOCKER ?)


--PARTIE X - CALCUL DE LA PREVISION UNE FOIS TOUTES LES SIMILARITES CALCULEES




