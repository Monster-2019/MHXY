#!/bin/sh

python -m eel main.py web/dist --add-data "images:images" --add-data "config.ini:." --noconfirm --noconsole --name mhxy_script

if [[ ! $(uname -sr) == MINGW* ]]; then
    echo not windows
    ls
    cd dist
    ls
    zip mhxy_script.zip mhxy_script
else 
    echo is windows
fi