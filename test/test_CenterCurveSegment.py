#!/usr/bin/env python
# coding=utf-8

from inkex.tester import TestCase
from round_corners import CenterCurveSegment

class CenterCurveTestCase(TestCase):
    def test_point_calculation(self):
        ccs = CenterCurveSegment(
            [-1, 1, -1, 1],
            [-1, -1, 1, 1],
            1,
            0.5,
            0.01,
            0,
            1
        )
        self.assertAlmostEqual(ccs.p_start, (-1, -0.5))
        self.assertAlmostEqual(ccs.p_end, (1, 1.5))
        self.assertAlmostEqual(ccs.calculate_center_point(0.5), (-0.5, 0))
