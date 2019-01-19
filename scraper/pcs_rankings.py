#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import json
import time
import os

import requests
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://www.procyclingstats.com/'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Output file')
    parser.add_argument('--paging', type=int, default=200, help='Number of entries to show (50, 100, 200)')
    parser.add_argument('--max-pages', type=int, default=10, help='Number of pages to scrape')
    parser.add_argument('--ranking-id', type=int, default=32741, help='Rank page id')
    parser.add_argument('--delay', type=float, default=1.0, help=argparse.SUPPRESS)
    parser.add_argument('--url',
                        type=str,
                        default=BASE_URL + 'rankings.php?id={ranking_id}&page={offset}&limit={limit}',
                        help=argparse.SUPPRESS)

    args = parser.parse_args()

    return args


def get_ranks(url):
    logging.info(f'loading data from {url}')
    resp = requests.get(url)
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
    args = parse_args()

    if os.path.exists(args.filename):
        logging.warn(f'"{args.filename}" alredy exists')

    complete_ranks = {}
    for offset in range(0, args.max_pages * args.paging, args.paging):
        html = get_ranks(args.url.format(ranking_id=args.ranking_id, offset=offset, limit=args.paging))
        ranks = parse_ranks(html)
        if len(ranks) == 0:
            logging.debug(f'found zero results trying to read {args.paging} entries from position {offset}')
            break
        complete_ranks.update(ranks)
        time.sleep(args.delay)

    with open(args.filename, 'w') as out:
        json.dump(complete_ranks, out, sort_keys=True, indent=4)
        logging.info(f'saved {len(complete_ranks)} riders into "{args.filename}"')


if __name__ == '__main__':
    main()
