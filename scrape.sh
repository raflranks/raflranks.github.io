#!/usr/bin/env sh
set -e
set -x

today=$(date +%Y-%m-%d)
scores_file="./data/scores.json"
scores_file_new="scores.$today.json"
ranks_file="./data/raw/ranks.$today.json"

rafl-scrape $ranks_file
rafl-scores --last-ranks $ranks_file --scores $scores_file --output-file $scores_file_new
mv $scores_file "./data/backup/$scores_file_new"
mv $scores_file_new $scores_file

git status