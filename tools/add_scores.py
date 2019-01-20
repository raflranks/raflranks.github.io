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


def calculate_week_diff(week_data, new_scores, new_week_number):
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


def verify_totals(current, totals):
    if len(current) != len(totals):
        raise ValueError('Missing riders')

    for rider, score in current.items():
        if totals[rider] != score:
            raise ValueError(f'Rider "{rider}" has invalid score ({score})')


def main():
    args = parse_args()
    print(f'Processing week {args.week}')

    with open(args.scores) as f:
        scores = json.load(f)
        print(f'Loaded scores with {len(scores["weekly_data"])} weeks covered')

    with open(args.last_ranks, 'r') as f:
        ranks = json.load(f)

    diff = calculate_week_diff(scores['weekly_data'][:args.week], ranks, args.week)
    scores['weekly_data'].append({
        'week_number': args.week,
        'scores': diff,
        })

    totals = calculate_totals(scores['weekly_data'])
    verify_totals(ranks, totals)
    scores['totals'] = totals

    with open(f'{args.scores}.new', 'w') as f:
        json.dump(scores, f, sort_keys=True, indent=4)
        print(f'Saved scores for {len(totals)} riders')


if __name__ == '__main__':
    main()
