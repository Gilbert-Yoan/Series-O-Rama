---------------------------------DEBUT DE LA RECOMMANDATION POUR UN UTILISATEUR PRECIS---------------------------------------------------
--Récupérer uniquement les séries que l'utilisateur (ici le 3) n'a pas encore notéeS (donc pas vue)

--les paramètres marchent différemment en POSTGRESQL et nous n'en avons pas besoin maintenant
(SELECT ids FROM Serie )
EXCEPT
(SELECT ids FROM NOTER
WHERE idu=1) ; --attendu 1


--Pour chaque série non notée par l'utilisateur N (ici 3) on va calculer la note qu'il pourrait donner
--en fonction des notes déjà données pour cette série par d'autres utilisateurs par rapport aux séries en commun avec l'utilisateur 3
--On devra ensuite décider en fonction de la note prédite si on propose ou non la série

--PARTIE 1 - RECUPERER LES UTILISATEURS (QUI ONT VUE LA SERIE 1 ET QUI ONT DES SERIES EN COMMUN AVEC L'UTILISATEUR 3) 
SELECT DISTINCT idu
FROM NOTER
WHERE ids IN (SELECT ids FROM NOTER WHERE idu = 3) AND idu != 3; 


--PARTIE 2 - POUR CHAQUE UTILISATEUR
    --PARTIE 2.1 - CALCUL DE LA MOYENNE DES NOTES
    WITH MOYENNES AS (SELECT idu, AVG(note) FROM NOTER GROUP BY idu)
	SELECT * FROM MOYENNES WHERE idu IN (SELECT idu FROM NOTER WHERE ids IN (SELECT ids FROM NOTER WHERE idu=3));

    --PARTIE 2.2 - ON RETRANCHE A CHAQUE NOTE DE SERIE LA MOYENNE (A STOCKER ?)
    WITH MOYENNES AS (SELECT idu, AVG(note) AS moy FROM NOTER GROUP BY idu)
	SELECT m.idu,n.ids, note-moy FROM NOTER n, MOYENNES m 
    WHERE m.idu IN (SELECT idu FROM NOTER WHERE ids IN (SELECT ids FROM NOTER WHERE idu=3))
    AND m.idu = n.idu;

    --PARTIE 2.3 - CALCUL DE LA SIMILARITE
    WITH MOYENNES AS (SELECT idu, AVG(note) AS moy FROM NOTER GROUP BY idu),

        NOTES_RETRANCHES AS (
            SELECT m.idu,n.ids, note-moy AS note FROM NOTER n, MOYENNES m 
            WHERE m.idu IN (SELECT idu FROM NOTER WHERE ids IN (SELECT ids FROM NOTER WHERE idu=3))
            AND m.idu = n.idu),
        HAUT_SIMILARITES AS (
            SELECT SUM(n.note*n2.note)as somme,n.idu 
            FROM NOTES_RETRANCHES n, NOTES_RETRANCHES n2 
            WHERE n.idu!=n2.idu AND n2.idu=3 AND n.ids=n2.ids 
            GROUP BY n.idu),
        BAS_SIMILARITES AS (
            SELECT SQRT(SUM(POWER(n.note,2))*SUM(POWER(n2.note,2))) as racine, n.idu 
            FROM NOTES_RETRANCHES n, NOTES_RETRANCHES n2 
            WHERE n.idu!=n2.idu AND n2.idu=3 AND n.ids=n2.ids
            GROUP BY n.idu)
        SELECT somme/racine FROM HAUT_SIMILARITES h,BAS_SIMILARITES b WHERE h.idu=b.idu;

--PARTIE 3 - CALCUL DE LA PREVISION UNE FOIS TOUTES LES SIMILARITES CALCULEES
    WITH MOYENNES AS (SELECT idu, AVG(note) AS moy FROM NOTER GROUP BY idu),

        NOTES_RETRANCHES AS (
            SELECT m.idu,n.ids, note-moy AS note FROM NOTER n, MOYENNES m 
            WHERE m.idu IN (SELECT idu FROM NOTER WHERE ids IN (SELECT ids FROM NOTER WHERE idu=3))
            AND m.idu = n.idu),
        HAUT_SIMILARITES AS (
            SELECT SUM(n.note*n2.note)as somme,n.idu 
            FROM NOTES_RETRANCHES n, NOTES_RETRANCHES n2 
            WHERE n.idu!=n2.idu AND n2.idu=3 AND n.ids=n2.ids 
            GROUP BY n.idu),
        BAS_SIMILARITES AS (
            SELECT SQRT(SUM(POWER(n.note,2))*SUM(POWER(n2.note,2))) as racine, n.idu 
            FROM NOTES_RETRANCHES n, NOTES_RETRANCHES n2 
            WHERE n.idu!=n2.idu AND n2.idu=3 AND n.ids=n2.ids
            GROUP BY n.idu),
        SIMILARITES AS (SELECT somme/racine as similarite, h.idu FROM HAUT_SIMILARITES h,BAS_SIMILARITES b WHERE h.idu=b.idu),
        PARTIE_HAUTE AS (SELECT SUM(n.note*s.similarite) as haute FROM NOTES_RETRANCHES n, SIMILARITES s WHERE n.idu = s.idu AND n.ids = 1),
        SOMME_SIMILARITES AS (SELECT SUM(ABS(similarite)) as sim FROM SIMILARITES)
	    SELECT moy+(haute/sim) FROM MOYENNES m, PARTIE_HAUTE p, SOMME_SIMILARITES s WHERE m.idu = 3;

--https://www.postgresql.org/docs/9.1/queries-with.html

