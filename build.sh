#!/bin/bash

# Navigate to the directory where the script is located
cd "$(dirname "$0")" || exit

# Install the required Python packages
echo "Installing required packages..."
pip install -r requirements.txt
