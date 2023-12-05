#!/bin/bash
cd "$(dirname "$0")" || exit
python scrape_urls.py > url_test.txt
first_ten="temp_first_10.txt"
head -n 10 url_test.txt > "$first_ten"
python scrape_details.py "$first_ten"
rm "$first_ten"