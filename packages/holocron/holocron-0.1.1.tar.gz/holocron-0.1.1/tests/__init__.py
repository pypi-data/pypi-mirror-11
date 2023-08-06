# coding: utf-8
"""
    tests
    ~~~~~

    Tests Holocron itself.

    :copyright: (c) 2014 by the Holocron Team, see AUTHORS for details.
    :license: 3-clause BSD, see LICENSE for details.
"""

import sys
import logging
import unittest


class HolocronTestCase(unittest.TestCase):
    """
    Base class for all the tests that Holocron uses.
    """
    #: disable holocron's logging output during tests
    logging.disable(logging.CRITICAL)

    #: disable holocron's message output during tests
    sys.stdout = None
