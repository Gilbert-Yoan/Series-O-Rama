#!/bin/sh

#cherche les fichiers zip et affiche ahaha si 
 
dezipper()
{
	for file in `ls $1/*/*`
	do
		echo "$file" | grep -q ".zip";
		ret=$?;
		if [ "$ret" == 0 ]
		then
			homedir="$(dirname "$file")" 
			unzip -o "$file" -d "$homedir" ;
			rm "$file";
		fi
	done
	if [ `ls $1/* | grep -c ".zip"` -gt 0 ]
	then
	dezipper $1
	fi
}

##nécessaire de changer le caractère de retour à la ligne 
##pour les fichiers avec un espace dans le nom
##les fichiers avec \n dedans n'existe pas à priori après des test sur le terminal GNU

OIFS="$IFS"
IFS=$'\n'
dezipper $1 
IFS="$OIFS"
