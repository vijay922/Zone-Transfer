#!/bin/bash

mkdir -p Results
for url in $(cat "$1") 
do
    subfinder -d $url -all -t 200 > subdomains.txt
    timeout 2h python3 zonetransfer.py -l subdomains.txt > Results/$url-zone.txt
done
