#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import operator
import json


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--teams', required=True, help='File with teams')
    parser.add_argument('--scores', required=True, help='Score file')

    return parser.parse_args()


def pretty_name(name):
    return name.replace('_', ' ').capitalize()


def main():
    args = parse_args()

    with open(args.teams, 'r') as f:
        auctions = json.load(f)

    with open(args.scores, 'r') as f:
        scores = json.load(f)
        totals = scores['totals']

    for auction, teams in auctions.items():
        auction_total = 0
        print(f'Auction {auction}')
        for team in teams:
            print(f' Team {team["owner"]}')
            scorers = {}
            for rider in team['riders']:
                score = totals.get(rider, 0)
                if score > 0:
                    scorers[pretty_name(rider)] = score

            for rider, score in sorted(scorers.items(), key=operator.itemgetter(1)):
                print(f'  {rider} - {score} points')
            total = sum(scorers.values())
            auction_total += total
            print(f'  TOTAL    {total} points')
            print()

        print(f'{auction} auction TOTAL - {auction_total} points')
        print()


if __name__ == '__main__':
    main()
