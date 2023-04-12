#!/bin/sh

if [[ ! $(uname -sr) == MINGW* ]]; then
    echo not windows
    python -m eel main.py web/dist --add-data "images:images" --add-data "config.ini:." --add-data "config:config" --noconfirm --noconsole --uac-admin --name mhxy_script
else 
    echo is windows
    python -m eel main.py web/dist --add-data "images;images" --add-data "config.ini;." --add-data "config;config" --onefile --noconfirm --noconsole --uac-admin --name mhxy_script
fi