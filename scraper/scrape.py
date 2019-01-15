#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import sys
import os

import requests
from bs4 import BeautifulSoup as bs


ranks_url = 'https://www.procyclingstats.com/rankings/me/season/individual'


def get_ranks():
    logging.info(f'loading data from {ranks_url}')
    resp = requests.get(ranks_url)
    if not resp.ok:
        logging.error(f'failed to load rankings with code {resp.status_code}')
        resp.raise_for_status()

    logging.info(f'Done in {resp.elapsed}')

    return resp.text


def get_name_from_cell(cell):
    href = cell.a['href']
    _, name = href.split('/')
    return name


def get_points_from_cell(cell):
    return cell.a.text


def parse_ranks(html):
    soup = bs(html, 'html.parser')
    table = soup.find('table', class_="basic")

    ranks = {}
    for n, row in enumerate(table.tbody.find_all('tr')):
        cells = row.find_all('td')

        rider = get_name_from_cell(cells[3])
        points = get_points_from_cell(cells[5])

        if rider in ranks:
            logging.error('Rider "{rider}" already present')
            raise ValueError('Duplicit Entry')

        ranks[rider] = points

    return ranks


def main():
    if len(sys.argv) < 2:
        logging.error('missing argument: output filename')
        sys.exit(1)

    filename = sys.argv[1]
    if os.path.exists(filename):
        logging.warn(f'"{filename}" alredy exists')

    html = get_ranks()
    ranks = parse_ranks(html)

    with open(filename, 'w') as f:
        json.dump(ranks, f, sort_keys=True, indent=4)
        logging.info(f'saved {len(ranks)} riders into "{filename}"')


if __name__ == '__main__':
    main()    
