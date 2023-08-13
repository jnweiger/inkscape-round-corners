#!/usr/bin/env python
# coding=utf-8

import math
from inkex.tester import TestCase
from round_corners import CenterCurveSegment, intersectCenterCurveSegments

class CenterCurveTestCase(TestCase):
    def test_point_calculation(self):
        s = CenterCurveSegment(
            [-1, 1, -1, 1],
            [-1, -1, 1, 1],
            1,
            0.5,
            0.01,
            0,
            1
        )
        self.assertAlmostEqual(s._p_start, (-1, -0.5))
        self.assertAlmostEqual(s._p_end, (1, 1.5))
        self.assertAlmostEqual(s.calculate_center_point(0.5), (-0.5, 0))
        self.assertLessEqual(s._terminalSegments, 30)
        self.assertAlmostEqual(s._searchDir, (1/math.sqrt(2), 1/math.sqrt(2)))
        self.assertLess(s._searchValues[0], -1.060)
        self.assertGreater(s._searchValues[1], 1.767)
        self.assertLess(s._searchValues[2], 0.092)
        self.assertGreater(s._searchValues[3], 0.908)

    def test_empty_intersection(self):
        # the two segments are far away of each other.
        # empty intersection should be found immediately.
        s1 = CenterCurveSegment(
            [-1, 1, -1, 1],
            [-1, -1, 1, 1],
            1,
            0.5,
            0.01,
            0,
            1
        )
        s2 = CenterCurveSegment(
            [-1, 1, -1, 1],
            [-1+5, -1+5, 1+5, 1+5],
            1,
            0.5,
            0.01,
            0,
            1
        )
        ret = intersectCenterCurveSegments(s1, s2)
        self.assertEqual(ret, None)