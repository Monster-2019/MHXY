#!/bin/sh

pip install pyinstaller

python -m eel main.py web/dist --add-data "images;images" --add-data "config.ini;config.ini" --name mhxy_script

cd dist/
zip -r mhxy_script.zip mhxy_script
cd ..