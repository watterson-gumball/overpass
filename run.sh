#!/bin/bash

app_dir=$(find /opt/overpass/ -maxdepth 1 -type d -name "osm-3s_v*" | head -n 1)

cd $app_dir

rm -f "$app_dir"/db/osm3s_areas "$app_dir"/db/osm3s_osm_base

cd /opt/overpass

nohup bin/dispatcher --osm-base --attic --db-dir="/opt/overpass/db" --allow-duplicate-queries=yes &
nohup bin/dispatcher --areas --db-dir="/opt/overpass/db" --allow-duplicate-queries=yes &
bin/rules_loop.sh "db" &

a2enmod cgid
a2enmod ext_filter
a2enmod headers

service apache2 restart

tail -f /dev/null