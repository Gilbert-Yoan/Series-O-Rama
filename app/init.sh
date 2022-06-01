#!/bin/sh

#2 passages pour etre sur de ne pas louper des fichiers imbriqués
#Ce nombre de passages est empirique par rapport à la source fournie

./preprocessing/unzip.sh ./preprocessing/sous-titres &
wait $!
./preprocessing/unfold.sh ./preprocessing/sous-titres &
wait $!
./preprocessing/unzip.sh ./preprocessing/sous-titres &
wait $!
./preprocessing/unfold.sh ./preprocessing/sous-titres &
wait $!

#Creation de la BDD et peuplement
python3 ./BDD/init_db.py &
wait $!
python3 ./preprocessing/preprocessing_chargementBDD.py ./preprocessing/sous-titres
