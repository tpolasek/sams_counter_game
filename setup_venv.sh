#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate and install
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment created and dependencies installed!"
echo "Activate with: source venv/bin/activate"
