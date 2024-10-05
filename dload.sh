#!/bin/bash

if [ ! -d "./description/$2" ]
then 
	mkdir ./description/$2
fi

if [ ! -d "./description/$2/$3" ]
then
        mkdir ./description/$2/$3
fi

c=0
cat $1 | while read line
do
	echo "Downloading:${line}"
	if [ ! -d "./description/$2/$3/$((c/100))" ]
	then
		mkdir ./description/$2/$3/$((c/100))
	fi
	curl -k https://patents.google.com/patent/${line} > ./description/$2/$3/$((c/100))/${line}.html
	let c++
done
