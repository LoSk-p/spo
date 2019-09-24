#!/bin/bash
dir=~/6  #Исследуемая директория
rm $dir/lab1.xls
mkdir ~/vspom
cd ~/vspom

IFS=$'\n'
files=$( find $dir -type f )
for file in $files; do 
echo "$file" | awk -F "/" '{print $NF}' |  awk -F "." '{if (NF==1) {print $0,"-"} else {print $0,$NF}}' OFS=',' >> name.txt
stat --format=%s "$file" >> size.txt
stat --format=%y "$file" >> times.txt
file --mime-type -b  "$file" >> type.txt
lek=$(mediainfo "$file" 2>/dev/null | grep --max-count=1 Duration | awk '{print $3,$4}') 
echo -"$lek" >> duration.txt
done

echo Имя,Расширение,Размер,Время изменения,Тип,Длительность > $dir/lab1.xls
paste --delimiters=',' name.txt size.txt times.txt type.txt duration.txt >> $dir/lab1.xls

cd $dir
rm -r ~/vspom
