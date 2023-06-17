#!/bin/sh

if [[ ! $(uname -sr) == MINGW* ]]; then
    echo not windows
    pyinstaller main.py --add-data "images:images" --add-data "config.ini:." --add-data "config:config" --add-data "tesseract;tesseract" --noconfirm --uac-admin --name mhxy_script
else 
    echo is windows
    pyinstaller main.py --add-data "images;images" --add-data "config.ini;." --add-data "config;config" --add-data "tesseract;tesseract" --noconfirm --uac-admin --name mhxy_script
fi