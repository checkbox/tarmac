# Copyright (c) 2009 - Paul Hummer
'''Tests for Tarmac scripts.'''
import os
import sys
import unittest

from tarmac.bin import TarmacLander


class TestTarmacLander(unittest.TestCase):
    '''Tests for TarmacLander.'''

    def test_lander_dry_run(self):
        '''Test that setting --dry-run sets the dry_run property.'''
        sys.argv = ['foo', '--dry-run']
        script = TarmacLander()
        self.assertTrue(script.dry_run)

