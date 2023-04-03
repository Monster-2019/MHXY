#!/bin/sh

python -m eel main.py web/dist --add-data "images:images" --add-data "config.ini:." --noconfirm --noconsole --name mhxy_script

if [[ ! $(uname -sr) == MINGW* ]]; then
    echo not windows
    zip -r mhxy_script.zip . -i dist/mhxy_script
else 
    echo is windows
fi