#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

from fuzzywuzzy import process


class NameConverter:
    def __init__(self, names, threshold=0.8):
        self.names = names
        self.threshold = threshold
        self.cache = {}

    def fix_name(self, name):
        name = self._normalize_name(name)
        if name in self.cache:
            return self.cache[name]

        fixed_name = self.find_match(name)
        self.cache[name] = fixed_name

        return fixed_name

    def find_match(self, name):
        match, score = process.extractOne(name, self.names)
        if score < self.threshold:
            raise ValueError(f'Uknown rider "{name}"')
        return match

    @staticmethod
    def _normalize_name(name):
        return name.lower()


def main():
    teams_file = sys.argv[1]
    keys_file = sys.argv[2]

    with open(keys_file, 'r') as r:
        names = json.load(r)

    with open(teams_file, 'r') as r:
        auctions = json.load(r)

    converter = NameConverter(names.keys())
    for auction_name, teams in auctions.items():
        print(auction_name)
        for team in teams:
            print('\t', team['owner'])
            riders_fixed = {}
            for rider, score in team['riders'].items():
                print(rider, end=', ')
                riders_fixed[converter.fix_name(rider)] = score
            team['riders'] = riders_fixed
            print('DONE')

    with open(f'{teams_file}.fixed', 'w') as f:
        json.dump(auctions, f)


if __name__ == '__main__':
    main()
