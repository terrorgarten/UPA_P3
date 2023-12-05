#!/bin/bash
cd "$(dirname "$0")" || exit
echo "Installing required packages..."
pip install -r requirements.txt
echo "All set up for scraping!"
