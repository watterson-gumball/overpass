#!/bin/bash

INSTALLATION_DIR='/opt/overpass'
ARCHIVE='osm-3s_latest.tar.gz'
SOURCE_URL="https://dev.overpass-api.de/releases/$ARCHIVE"

mkdir $INSTALLATION_DIR
cd $INSTALLATION_DIR
wget $SOURCE_URL
tar -xzf $ARCHIVE

app_dir=$(find $INSTALLATION_DIR -maxdepth 1 -type d -name "osm-3s_v*" | head -n 1)

cd $app_dir
./configure --enable-lz4
make
chmod 755 bin/*.sh cgi-bin/*
cp -r "$app_dir/bin" "$INSTALLATION_DIR/"
cp -r "$app_dir/cgi-bin" "$INSTALLATION_DIR/"

db_dir="$INSTALLATION_DIR/db"
mkdir $db_dir
cp -r "$app_dir/rules" "$db_dir/"

cat /data.osm | "$app_dir/bin/update_database" --db-dir="$db_dir/" --meta=attic