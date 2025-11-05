#!/usr/bin/env bash
set -e

# Name of the venv folder
VENV_DIR="./home/ak562fx/ss"

echo "Creating virtual environment in $VENV_DIR ..."
python3 -m venv $VENV_DIR

echo "Activating virtual environment ..."
source $VENV_DIR/bin/activate

echo "Upgrading pip ..."
pip install --upgrade pip

if [ -f requirements.txt ]; then
  echo "Installing requirements ..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found, skipping install."
fi

echo "Environment ready. To activate later, run:"
echo "source $VENV_DIR/bin/activate"
