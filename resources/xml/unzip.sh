#!/bin/bash
IFS=$'\n'
for i in *.zip
do
   for n in $(unzip -Z -1 "$i"); do 
       echo "$i - $n"
       e=${n#*.}
       unzip "$i" "$n" && mv "$n" ${i%%.*}".$e"
   done
   rm $i
done