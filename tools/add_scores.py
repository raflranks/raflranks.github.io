#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import argparse
import datetime
import logging
import json
import os


def current_week():
    return datetime.date.today().isocalendar()[1]


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--last-ranks', required=True, help='File with latest ranks')
    parser.add_argument('--scores', required=True, help='Score file')
    parser.add_argument('--output-file', required=True, help='Output file for new scores')
    parser.add_argument('--week', type=int, default=current_week(), help=argparse.SUPPRESS)
    parser.add_argument('--no-totals', action='store_true', default=False, help='Do not overwrite totals')

    return parser.parse_args()


def calculate_totals(week_data):
    totals = defaultdict(int)
    for week_number, week in enumerate(week_data):
        if week['week_number'] != week_number:
            logging.error(f'Incomplete week series at {week_number} of {len(week_data)}')
            raise ValueError('Incomplete week data')

        scores = week['scores']
        for rider, score in scores.items():
            totals[rider] += score

    return totals


def calculate_week_diff(week_data, new_scores, new_week_number):
    if new_week_number != (week_data[-1]['week_number'] + 1):
        logging.error(f'New week ({new_week_number}) does not follow last week in series')
        raise ValueError('Invalid week data')

    totals = calculate_totals(week_data)

    diff_scores = {r: s for r, s in new_scores.items() if r not in totals}
    for rider, score in totals.items():
        diff = new_scores[rider] - score
        if diff != 0:
            # if diff < 0:
            #     logging.warning(f'"{rider}" has lower score in week {new_week_number}')
            diff_scores[rider] = diff

    return diff_scores


def verify_totals(current, totals):
    if len(current) != len(totals):
        logging.error('Missing riders in either totals or weekly data')
        raise ValueError('Invalid score data')

    for rider, score in current.items():
        if totals[rider] != score:
            logging.error(f'Rider "{rider}" has invalid score ({score})')
            raise ValueError('Invalid score')


def main():
    args = parse_args()
    logging.info(f'Processing week {args.week}')

    with open(args.scores) as f:
        scores = json.load(f)
        logging.info(f'Loaded scores with {len(scores["weekly_data"])} weeks covered')

    with open(args.last_ranks, 'r') as f:
        ranks = json.load(f)

    diff = calculate_week_diff(scores['weekly_data'][:args.week], ranks, args.week)
    new_week_data = {
        'week_number': args.week,
        'scores': diff,
    }
    if len(scores['weekly_data']) >= args.week:
        # week update
        scores['weekly_data'][args.week] = new_week_data
    else:
        # new week
        scores['weekly_data'].append(new_week_data)

    totals = calculate_totals(scores['weekly_data'])
    verify_totals(ranks, totals)
    scores['totals'] = totals

    _, scores['_update_source'] = os.path.split(args.last_ranks)
    scores['_update_timestamp'] = datetime.datetime.now().isoformat()

    with open(f'{args.output_file}', 'w') as f:
        json.dump(scores, f, sort_keys=True, indent=4)
        logging.info(f'Saved scores for {len(totals)} riders')


if __name__ == '__main__':
    main()
