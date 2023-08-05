#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: 3 Clause BSD
# Part of Carpyncho - http://carpyncho.jbcabral.org


# =============================================================================
# DOCS
# =============================================================================

"""This file is for test carpyncho pytff

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import unittest
import tempfile
import shutil
import random

import six

import numpy as np

import pytff


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

DATA_PATH = os.path.join(PATH, "test_data")


# =============================================================================
# TEST CASES
# =============================================================================

class PyTFFFunctionTest(unittest.TestCase):

    def test_cache_hash(self):
        data = [
            six.text_type(random.random()),
            np.random.randn(10), six.b("hhh"), "hhh"
        ]
        for elem in data:
            pytff.cache_hash(elem)

    def test_loadtarget(self):
        data = "1 2\n3 4\n5 6"
        fp = six.StringIO(data)
        times_values = pytff.loadtarget(fp)
        for lidx, line in enumerate(data.splitlines()):
            for cidx, value in enumerate(line.split()):
                fvalue = float(value)
                pytff_value = times_values[cidx][0][lidx]
                np.testing.assert_allclose(fvalue, pytff_value)

    def test_stack_targets_diferent_sizes(self):
        # Diferent sizes
        times = [[0, 1, 2], [3, 4, 5, 6]]
        expected_times = np.array([[0., 1., 2., np.nan],
                                   [3., 4., 5., 6.]])

        values = [[0, 1, 2], [3, 4, 5, 7]]
        expected_values = np.array([[0., 1., 2., np.nan],
                                    [3., 4., 5., 7.]])

        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        # diferent sizes array
        times = [np.array([0, 1, 2]), np.array([3, 4, 5, 6])]
        values = [np.array([0, 1, 2]), np.array([3, 4, 5, 7])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        # more dimensions
        times = [np.array([[0, 1, 2]]), np.array([[3, 4, 5, 6]])]
        values = [np.array([[0, 1, 2]]), np.array([[3, 4, 5, 7]])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

    def test_stack_targets_same_sizes(self):
        times = [[0, 1, 2], [3, 4, 5]]
        expected_times = np.array([[0., 1., 2.],
                                   [3., 4., 5.]])

        values = [[0, 1, 2], [3, 4, 5]]
        expected_values = np.array([[0., 1., 2.],
                                    [3., 4., 5.]])

        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        # same sizes array
        times = [np.array([0, 1, 2]), np.array([3, 4, 5])]
        values = [np.array([0, 1, 2]), np.array([3, 4, 5])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        # arrays more dimensions
        times = [np.array([[0, 1, 2]]), np.array([[3, 4, 5]])]
        values = [np.array([[0, 1, 2]]), np.array([[3, 4, 5]])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

    def test_load_tff_dat(self):
        data_path = os.path.join(DATA_PATH, "single_dat")
        ogle_tff_path = os.path.join(data_path, "tff.dat")

        asstring = pytff.load_tff_dat(ogle_tff_path)
        with open(ogle_tff_path) as fp:
            asfp = pytff.load_tff_dat(fp)
        self.assertEquals(asstring, asfp)
        self.assertIsInstance(asstring, tuple)
        self.assertIsInstance(asfp, tuple)
        self.assertTrue(all(map(lambda e: isinstance(e, tuple), asstring)))
        self.assertTrue(all(map(lambda e: isinstance(e, tuple), asfp)))

        rnd = random.random()
        asstring = pytff.load_tff_dat(ogle_tff_path, lambda gen: rnd)
        with open(ogle_tff_path) as fp:
            asfp = pytff.load_tff_dat(fp, lambda gen: rnd)
        self.assertEquals(asstring, asfp)
        self.assertEquals(asfp, rnd)
        self.assertEquals(asstring, rnd)

    def test_load_match_dat(self):
        data_path = os.path.join(DATA_PATH, "single_dat")
        ogle_mch_path = os.path.join(data_path, "match.dat")

        asstring = pytff.load_match_dat(ogle_mch_path)
        with open(ogle_mch_path) as fp:
            asfp = pytff.load_match_dat(fp)
        self.assertEquals(asstring, asfp)
        self.assertIsInstance(asstring, tuple)
        self.assertIsInstance(asfp, tuple)
        self.assertTrue(all(map(lambda e: isinstance(e, tuple), asstring)))
        self.assertTrue(all(map(lambda e: isinstance(e, tuple), asfp)))

        rnd = random.random()
        asstring = pytff.load_match_dat(ogle_mch_path, lambda gen: rnd)
        with open(ogle_mch_path) as fp:
            asfp = pytff.load_match_dat(fp, lambda gen: rnd)
        self.assertEquals(asstring, asfp)
        self.assertEquals(asfp, rnd)
        self.assertEquals(asstring, rnd)


class PyTFFCommandTest(unittest.TestCase):

    def setUp(self):
        self.tff = pytff.TFFCommand()

    def test_single_data(self):
        data_path = os.path.join(DATA_PATH, "single_dat")
        ogle_path = os.path.join(data_path, "ogle.dat")
        ogle_tff_path = os.path.join(data_path, "tff.dat")
        ogle_dff_path = os.path.join(data_path, "dff.dat")
        ogle_mch_path = os.path.join(data_path, "match.dat")

        ogle_tff = pytff.load_tff_dat(ogle_tff_path, self.tff.process_tff)
        ogle_dff = pytff.load_tff_dat(ogle_dff_path, self.tff.process_dff)
        ogle_mch = pytff.load_match_dat(ogle_mch_path, self.tff.process_matchs)

        times, values = pytff.loadtarget(ogle_path)
        periods = np.array([0.6347522])

        tff_data, dff_data, mch_data = self.tff.analyze(periods, times, values)

        np.testing.assert_array_equal(tff_data, ogle_tff)
        np.testing.assert_array_equal(dff_data, ogle_dff)
        np.testing.assert_array_equal(mch_data, ogle_mch)

    def test_split_data(self):
        data_path = os.path.join(DATA_PATH, "split_dat")
        ogle_0_path = os.path.join(data_path, "ogle_0.dat")
        ogle_1_path = os.path.join(data_path, "ogle_1.dat")
        ogle_tff_path = os.path.join(data_path, "tff.dat")
        ogle_dff_path = os.path.join(data_path, "dff.dat")
        ogle_mch_path = os.path.join(data_path, "match.dat")

        ogle_tff = pytff.load_tff_dat(ogle_tff_path, self.tff.process_tff)
        ogle_dff = pytff.load_tff_dat(ogle_dff_path, self.tff.process_dff)
        ogle_mch = pytff.load_match_dat(ogle_mch_path, self.tff.process_matchs)

        times_0, values_0 = pytff.loadtarget(ogle_0_path)
        times_1, values_1 = pytff.loadtarget(ogle_1_path)
        times, values = pytff.stack_targets(
            (times_0, times_1), (values_0, values_1))
        periods = np.array([0.6347522] * 2)

        tff_data, dff_data, mch_data = self.tff.analyze(periods, times, values)

        np.testing.assert_array_equal(tff_data, ogle_tff)
        np.testing.assert_array_equal(dff_data, ogle_dff)
        np.testing.assert_array_equal(mch_data, ogle_mch)

    def test_diferent_shape_data(self):
        # this test only verify nothing blows up
        periods = [1, 2]
        times = [[0, 1, 2], [3, 4, 5, 6]]
        values = [[0, 1, 2], [3, 4, 5, 7]]
        self.tff.analyze(periods, times, values)

    def test_wrkpath_is_removed_when_is_temp(self):
        # remove clasic temp
        path = self.tff.wrk_path
        self.assertTrue(os.path.exists(path) and os.path.isdir(path))
        del self.tff
        self.assertFalse(os.path.exists(path) and os.path.isdir(path))

    def test_wrkpath_is_not_removed_when_is_not_temp(self):
        path = tempfile.mkdtemp(suffix="_tff_test")

        self.tff = pytff.TFFCommand(wrk_path=path)
        self.assertTrue(os.path.exists(path) and os.path.isdir(path))
        del self.tff
        self.assertTrue(os.path.exists(path) and os.path.isdir(path))

        shutil.rmtree(path, True)

    def test_write_stk_targets(self):
        periods = [1, 2]
        times = [[0, 1, 2], [3, 4, 5, 6]]
        values = [[0, 1, 2], [3, 4, 5, 7]]
        self.tff.debug = True
        self.tff.analyze(periods, times, values)

        targets = np.dstack(pytff.stack_targets(times, values))
        for idx, t in enumerate(targets):
            ch = pytff.cache_hash(t)
            self.assertIn(ch, self.tff.targets_cache)
            with open(self.tff.targets_cache[ch]) as fp:
                linenos = len(fp.readlines())
            self.assertTrue(len(times[idx]) == len(values[idx]) == linenos)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    unittest.main()
