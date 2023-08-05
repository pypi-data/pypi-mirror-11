from __future__ import division
import unittest
from unittest import TestCase

import numpy as np

from multihist import Hist1d, Hist2d

n_bins = 100
test_range = (-3, 4)


class TestHist1d(TestCase):

    def setUp(self):
        self.m = Hist1d(bins=n_bins, range=test_range)

    def test_is_instance(self):
        self.assertIsInstance(self.m, Hist1d)

    def test_list_like_access(self):
        m = self.m
        self.assertEqual(m[3], 0)
        self.assertEqual(m[3:5].tolist(), [0, 0])
        m[3] = 6
        self.assertEqual(m[3], 6)
        m[3:5] = [4, 3]
        self.assertEqual(m[3:5].tolist(), [4, 3])
        self.assertEqual(len(m), 100)

    def test_iteritems(self):
        m = self.m
        it = m.items()
        self.assertEqual(next(it), (-2.965, 0))

    def test_init_from_data(self):
        ex_data = list(range(11))
        m = Hist1d(ex_data, bins=len(ex_data) - 1)
        self.assertEqual(m.bin_edges.tolist(), ex_data)
        self.assertTrue(m.histogram.tolist(), [1]*n_bins)

    def test_init_from_histogram(self):
        m = Hist1d.from_histogram([0, 1, 0], [0, 1, 2, 3])
        self.assertEqual(m.histogram.tolist(), [0, 1, 0])
        self.assertEqual(m.bin_centers.tolist(), [0.5, 1.5, 2.5])

    def test_add_data(self):
        m = self.m
        m.add([0, 3, 4])
        self.assertEqual(m.histogram.tolist(),
                         np.histogram([0, 3, 4],
                                      bins=n_bins, range=test_range)[0].tolist())
        m.add([0, 3, 4])
        self.assertEqual(m.histogram.tolist(),
                         np.histogram([0, 3, 4]*2,
                                      bins=n_bins, range=test_range)[0].tolist())
        m.add([0, 3, 4, 538])
        self.assertEqual(m.histogram.tolist(),
                         np.histogram([0, 3, 4]*3,
                                      bins=n_bins, range=test_range)[0].tolist())

    def test_overload(self):
        m = self.m
        m.add([test_range[0]])
        m2 = self.m + self.m
        self.assertEqual(m2.histogram[0], [2])
        self.assertEqual(m2.histogram[1], [0])
        self.assertEqual(m2.bin_edges.tolist(), m.bin_edges.tolist())

test_range_2d = ((-1, 1), (-10, 10))
test_bins_2d = 3


class TestHist2d(TestCase):

    def setUp(self):
        self.m = Hist2d(range=test_range_2d, bins=test_bins_2d)

    def test_is_instance(self):
        self.assertIsInstance(self.m, Hist2d)

    def test_add_data(self):
        m = self.m
        x = [0.1, 0.8, -0.4]
        y = [0, 0, 0]
        m.add(x, y)
        self.assertEqual(m.histogram.tolist(),
                         np.histogram2d(x, y,
                                        range=test_range_2d,
                                        bins=test_bins_2d)[0].tolist())
        m.add(x, y)
        self.assertEqual(m.histogram.tolist(),
                         np.histogram2d(x*2, y*2,
                                        range=test_range_2d,
                                        bins=test_bins_2d)[0].tolist())
        m.add(x + [99999], y + [999999])
        self.assertEqual(m.histogram.tolist(),
                         np.histogram2d(x*3, y*3,
                                        range=test_range_2d,
                                        bins=test_bins_2d)[0].tolist())

    def test_slice(self):
        m = self.m
        x = [0.1, 0.8, -0.4]
        y = [0, 0, 0]
        m.add(x, y)
        s1 = m.slice(0, axis='y')
        self.assertIsInstance(s1, Hist1d)
        self.assertEqual(s1.histogram.tolist(), [1, 1, 1])
        s2 = m.slice(0, axis='x')
        self.assertEqual(s2.histogram.tolist(), [0, 1, 0])

    def test_projection(self):
        m = self.m
        x = [0.1, 0.8, -0.4]
        y = [0, 0, 0]
        m.add(x, y)
        p1 = m.projection('x')
        self.assertEqual(p1.histogram.tolist(), [1, 1, 1])
        self.assertAlmostEqual(np.sum(p1.bin_edges - np.array([-1, -1/3, 1/3, 1])), 0)
        p2 = m.projection('y')
        self.assertEqual(p2.histogram.tolist(), [0, 3, 0])
        self.assertAlmostEqual(np.sum(p2.bin_edges - np.array([-1, -1/3, 1/3, 1])), 0)


if __name__ == '__main__':
    unittest.main()
