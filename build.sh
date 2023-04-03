#!/bin/sh

if [[ ! $(uname -sr) == MINGW* ]]; then
    echo not windows
    pwd
    python -m eel main.py web/dist --add-data "images:images" --add-data "config.ini:." --noconfirm --noconsole --name mhxy_script
    ls
    cd dist
    ls
    zip mhxy_script.zip mhxy_script
else 
    python -m eel main.py web/dist --add-data "images;images" --add-data "config.ini;." --noconfirm --noconsole --name mhxy_script
    echo is windows
fi