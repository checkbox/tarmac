# Copyright 2009 Paul Hummer - See LICENSE
'''Tests for tarmac.branch'''
import unittest

from tarmac import branch


class TestBranch(unittest.TestCase):
    '''Test for Tarmac.branch.Branch.'''

    def test_create(self):
        '''Test the creation of a TarmacBranch instance.'''
        b = branch.Branch()
        self.assertTrue(isinstance(b, branch.Branch))

