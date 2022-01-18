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

--https://www.postgresql.org/docs/9.1/queries-with.html

