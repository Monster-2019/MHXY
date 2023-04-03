#!/bin/sh

pip install pyinstaller

python -m eel main.py web/dist --add-data "images;images" --add-data "config.ini;config.ini" --noconfirm --noconsole --name mhxy_script

if [[ ! $(uname -sr) == MINGW* ]]; then
    echo not windows
    cd dist/
    zip -r mhxy_script.zip mhxy_script
    cd ..
else 
    echo is windows
fi