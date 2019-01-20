#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import argparse
import datetime
import json


def current_week():
    return datetime.date.today().isocalendar()[1]


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--last-ranks', required=True, help='File with latest ranks')
    parser.add_argument('--scores', required=True, help='Score file')
    parser.add_argument('--week', type=int, default=current_week(), help=argparse.SUPPRESS)
    parser.add_argument('--no-totals', action='store_true', default=False, help='Do not overwrite totals')

    return parser.parse_args()


def calculate_totals(week_data):
    totals = defaultdict(int)
    for week_number, week in enumerate(week_data):
        if week['week_number'] != week_number:
            raise ValueError(f'Incomplete week series at {week_number} of {len(week_data)}')

        scores = week['scores']
        for rider, score in scores.items():
            totals[rider] += score

    return totals


def calulate_week_diff(week_data, new_scores, new_week_number):
    if new_week_number != (week_data[-1]['week_number'] + 1):
        raise ValueError(f'New week ({new_week_number}) does not follow last week in series')

    totals = calculate_totals(week_data)

    diff_scores = {r: s for r, s in new_scores.items() if r not in totals}
    for rider, score in totals.items():
        diff = new_scores[rider] - score
        if diff != 0:
            # if diff < 0:
            #     print(f'Warning: "{rider}" has lower score in week {new_week_number}')
            diff_scores[rider] = diff

    return diff_scores


def main():
    args = parse_args()

    with open(args.last_ranks, 'r') as f:
        ranks = json.load(f)

    with open(args.scores) as f:
        scores = json.load(f)
        print(f'Loaded scores with {len(scores["weekly_data"])} weeks covered, currently processing week {args.week}')


if __name__ == '__main__':
    main()
