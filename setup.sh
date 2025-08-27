#!/bin/bash
# Created by Nelson Durrant, Feb 2025
#
# Sets up the script to run automatically on Linux or WSL machines

if grep -q 'source ~/fly_fish_report/venv/bin/activate && python3 ~/fly_fish_report/fly_fish_report.py && deactivate' ~/.bashrc; then
    echo '[WARNING] The 'fly_fish_report.py' script is already found in the .bashrc'
else
    echo 'source ~/fly_fish_report/venv/bin/activate && python3 ~/fly_fish_report/fly_fish_report.py && deactivate' >> ~/.bashrc
fi