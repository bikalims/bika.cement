# -*- coding: utf-8 -*-
#
# This file is part of BIKA.CEMENT
#
# Copyright 2018 by it's authors.

import doctest

from .base import SimpleTestCase
from bika.cement.config import PRODUCT_NAME
from pkg_resources import resource_listdir
from os.path import join
from Testing import ZopeTestCase as ztc
import unittest2 as unittest

rst_filenames = [f for f in resource_listdir(PRODUCT_NAME, "tests/doctests")
                 if f.endswith(".rst")]

doctests = [join("doctests", filename) for filename in rst_filenames]

flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF


def test_suite():
    suite = unittest.TestSuite()
    for doctestfile in doctests:
        suite.addTests([
            ztc.ZopeDocFileSuite(
                doctestfile,
                test_class=SimpleTestCase,
                optionflags=flags,
            ),
        ])
    return suite
