#!/usr/bin/env python
# coding=utf-8
"""
Test elements extra logic from svg xml lxml custom classes.
"""

from inkex.tester import TestCase
from inkex.tester.inx import InxMixin

from my_effect_extension import UnnamedEffectExtension

import sys
sys.path.insert(0, '.')

class UnnamedBasicTestCase(InxMixin, TestCase):
    """Test INX files and other things"""
    def test_inx_file(self):
        """Get all inx files and test each of them"""
        self.assertInxIsGood("tutorial_01.inx")

    def test_other_things(self):
        """Things work out"""
        pass

class UnnamedComparisonsTestCase(ComparisonMixin, TestCase):
    """Test input and output variations"""
    effect_class = UnnamedEffectExtension
    comparisons = [
        ('--my_option=True',),
        ('--my_option=False',),
    ]
