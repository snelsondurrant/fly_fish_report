#!/bin/bash
# Created by Nelson Durrant, Feb 2025
#
# Sets up the virtual environment and configures the script to run automatically

cd ~/fly_fish_report
if [ -d "venv" ]; then
    echo "[INFO] Virtual environment already exists. Skipping setup."
else
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv

    echo "[INFO] Installing packages from requirements.txt..."
    source venv/bin/activate && pip install -r requirements.txt && deactivate
    echo "[SUCCESS] Environment created and packages installed."
fi

BASHRC_COMMAND='source ~/fly_fish_report/venv/bin/activate && python3 ~/fly_fish_report/fly_fish_report.py && deactivate'
if grep -Fxq "$BASHRC_COMMAND" ~/.bashrc; then
    echo "[WARNING] The script is already configured to run in .bashrc."
else
    echo "[INFO] Adding script to .bashrc..."
    echo '' >> ~/.bashrc
    echo '# Run the fly fishing report script on terminal launch' >> ~/.bashrc
    echo "$BASHRC_COMMAND" >> ~/.bashrc
    echo "[SUCCESS] .bashrc updated. Please run 'source ~/.bashrc' or restart your terminal."
fi