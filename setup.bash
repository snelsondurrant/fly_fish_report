#!/bin/bash
# Created by Nelson Durrant, Feb 2025

sudo apt install python3-requests
sudo apt install python3-bs4

if grep -q 'python3 ~/fishing_web_crawler/fishing.py' ~/.bashrc; then
    echo '[WARNING] Fly fishing script is already found in the .bashrc'
else
    echo 'python3 ~/fishing_web_crawler/fishing.py' >> ~/.bashrc
fi