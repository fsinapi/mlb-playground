#!/bin/bash

VENV_FOLDER=.venv

echo "Setting up virtual environment"
rm -f -r $VENV_FOLDER/
python3 -m venv $VENV_FOLDER
.  $VENV_FOLDER/bin/activate
echo "Installing packages"
pip install -r pipfile

mkdir -p data/
mkdir -p output/