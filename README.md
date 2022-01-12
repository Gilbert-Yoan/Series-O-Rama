# Series-O-Rama
## 🇬🇧 / 🇺🇸 : Tutored project from my Bachelor's last year in Big Data processing and management.  

This little website allows users to look for series with their own keywords. It also recommends series depending on the rating gave by the user to other series.

**On the technical side:**

The interest here is the way we handle .srt and .sub files in originally unorganized bulk folders to create the whole recommandation system.
Python scripts to read through these files have been developed and use the TF-IDF method to determine words without any importance. Those who add value are then stored in a PostGreSQL database.

## 🇫🇷 : Projet tuteuré réalisé lors de ma dernière année de Licence Professionnelle de Gestion et Traitement de Données Massives.

Ce site web permet aux utilisateurs de rechercher des séries avec leurs propres mots-clé. Ce site recommande aussi des series selon les notes données aux autres séries.

**Sur l'aspect technique:**

L'intérêt ici est la manière de gérer les fichiers .srt et .sub dans une masse de fichiers non organisée à l'origine afin de créer un système de recommandation.
Des scripts Python ont été développés pour lire à travers ces fichiers, ils utilisent la méthode TF-IDF afin de déterminer les mots sans importance. Ceux qui ont de la valeur sont alors stocké dans une base de données PostGreSQL. 
