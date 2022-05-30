------------------------RECOMMANDATION LEXICALE PAR RECUPERATION DES MOTS-CLES DES SERIES NOTEES----------------------------

--A FROID 
----Les mots cherchés par l'utilisateur doivent être enregistrés avec la date 
----Nous garderons les 5 derniers mots valides cherchés, un trigger s'occupera de vérifier et de supprimer ce qu'il faut
----CHERCHER(idu, idm, date)
----https://medium.com/@kay.schulz10/creating-a-recommender-system-without-user-information-cb4b3b60d4b0

SELECT s.ids, s.nomS, AVG(n.note) FROM serie s, contenir c, noter n 
WHERE c.ids = n.ids AND c.ids = s.ids 
AND c.idm IN (SELECT idm FROM CHERCHER WHERE idu=1)
GROUP BY s.ids, s.nomS;


--A FROID SANS RECHERCHE
----Selection de 20 séries au hasard

select * from serie order by random() limit 20;