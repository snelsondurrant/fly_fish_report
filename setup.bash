#!/bin/bash
# Created by Nelson Durrant, Feb 2025

sudo apt install python3-requests
sudo apt install python3-bs4

if grep -q 'python3 ~/fish_check/fish_check.py' ~/.bashrc; then
    echo '[WARNING] Fly fishing script is already found in the .bashrc'
else
    echo 'python3 ~/fish_check/fish_check.py' >> ~/.bashrc
fi