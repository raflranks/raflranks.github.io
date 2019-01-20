#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from .add_scores import calculate_totals, calculate_week_diff


class TestTools(unittest.TestCase):

    def setUp(self):
        self.test_week_data = [
            {'week_number': 0, 'scores': {'a': 1, 'b': 2, 'c': 3}},
            {'week_number': 1, 'scores': {'a': 1, 'x': 1, 'y': 1}},
            {'week_number': 2, 'scores': {}},
            {'week_number': 3, 'scores': {'a': 1, 'b': 5, 'z': 10, 'x': 1}},
        ]
        self.totals = {'a': 3, 'b': 7, 'z': 10, 'x': 2, 'c': 3, 'y': 1}

    def test_calculate_totlas_ok(self):
        expected = self.totals
        totals = calculate_totals(self.test_week_data)

        assert len(expected) == len(totals)
        assert all(totals[key] == score for key, score in expected.items())

    def test_calculate_totals_empty(self):
        assert calculate_totals({}) == {}

    def test_calculate_totals_skipped_week(self):
        data_skipped_week = [
            {'week_number': 0, 'scores': {'a': 1, 'b': 2, 'c': 3}},
            {'week_number': 2, 'scores': {'a': 1, 'x': 1, 'y': 1}},
        ]
        self.assertRaises(ValueError, lambda: calculate_totals(data_skipped_week))

    def test_calculate_totals_skipped_first_week(self):
        data_missing_first = [{'week_number': 1, 'scores': {'a': 1, 'x': 1, 'y': 1}}]
        self.assertRaises(ValueError, lambda: calculate_totals(data_missing_first))

    def test_calculate_week_diff_ok(self):
        next_week = {'a': 3, 'b': 10, 'z': 10, 'x': 5, 'c': 3, 'y': 1, 'w': 10}
        expected = {'b': 3, 'x': 3, 'w': 10}
        diff = calculate_week_diff(self.test_week_data, next_week, 4)
        assert expected == diff

    def test_calculate_week_diff_missing_riders(self):
        next_week = {'a': 3, 'b': 7, 'z': 10, 'x': 2, 'c': 3}
        self.assertRaises(KeyError, lambda: calculate_week_diff(self.test_week_data, next_week, 4))

    def test_calculate_week_diff_negative(self):
        next_week = self.totals
        next_week['b'] -= 6
        diff = calculate_week_diff(self.test_week_data, next_week, 4)
        assert diff == {'b': -6}

    def test_calculate_week_diff_wrong_week(self):
        next_week = self.totals
        self.assertRaises(ValueError, lambda: calculate_week_diff(self.test_week_data, next_week, 5))

    def test_calculate_week_diff_zero(self):
        next_week = self.totals
        diff = calculate_week_diff(self.test_week_data, next_week, 4)
        assert diff == {}
