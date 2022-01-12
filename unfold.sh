#!/bin/sh

#cherche les fichiers zip et affiche ahaha si 

##nécessaire de changer le caractère de retour à la ligne 
##pour les fichiers avec un espace dans le nom
##les fichiers avec \n dedans n'existent pas à priori après des test sur le terminal GNU

OIFS="$IFS"
IFS=$'\n'
for file in `find "$1" -mindepth 3`
do
	echo "hello";
	dest=`echo "$file" | cut -d '/' -f2`
	echo "$dest  à  $file";
	mv -f "$file" "$dest";
done

for rep in `find "$1" -mindepth 2 -type d`
do
	if [ $(ls -A "$rep" | wc -l) -eq 0 ]
	then
		rm -r "$rep";
	fi
done
IFS="$OIFS"
