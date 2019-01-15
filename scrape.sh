#!/usr/bin/env sh

today=$(date +%Y-%m-%d)
filename="ranks.$today.json"
file="./data/raw/$filename"

rafl-scrape $file
