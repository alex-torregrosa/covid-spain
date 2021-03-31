#!/bin/bash
tmp_dir="./tmp"

mkdir -p $tmp_dir
wget https://dadescovid.cat/static/csv/catalunya_diari_total_pob.zip -O $tmp_dir/cat.zip
wget https://cnecovid.isciii.es/covid19/resources/casos_tecnica_ccaa.csv -O $tmp_dir/spain.csv
unzip $tmp_dir/cat.zip -d $tmp_dir

vac_dir="$tmp_dir/vacunas"
mkdir -p $vac_dir
TODAY=`date -I`
d="2021-01-04"
until [[ $d > $TODAY ]]; do
    clean_d=`echo $d | sed 's/-//g'`
    (wget "https://covid-vacuna.app/data/$clean_d.json" -O "$vac_dir/$d.json" || rm "$vac_dir/$d.json")&
    d=$(date -I -d "$d + 1 day")
done
# Wait for downloads to complete
wait
rm ./tmp/cat.zip

