---------------------------------DEBUT DE LA RECHERCHE---------------------------------------------------
--Recherche par mots clés saisis et découpés au préalable dans une forme de liste SQL ('x','y','z',...)
--On compte le nombre de mots saisis qui correspondent à la série
--Puis on fait la somme des occurences de tous les mots qui ont matché 
--Les séries qui matchent le plus de mots et avec la plus grande occurence totale sont ressorties en premier
SELECT s.*, COUNT(s.ids), SUM(c.occurence) FROM SERIE s, CONTENIR c, MOTS m 
WHERE s.ids = c.ids AND m.idm = c.idm 
AND m.mot IN ('Sang','Police','GURLP','Magie') GROUP BY s.ids ORDER BY COUNT(s.ids) DESC,SUM(c.occurence) DESC; 

