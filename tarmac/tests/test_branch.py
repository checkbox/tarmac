# Copyright 2009 Paul Hummer - See LICENSE
'''Tests for tarmac.branch'''
import unittest

from bzrlib import branch as bzr_branch

from tarmac import branch
from tarmac.tests.mock import MockLPBranch


class TestBranch(unittest.TestCase):
    '''Test for Tarmac.branch.Branch.'''

    def test_create(self):
        '''Test the creation of a TarmacBranch instance.'''
        b = branch.Branch(MockLPBranch())

        self.assertTrue(isinstance(b, branch.Branch))
        self.assertTrue(isinstance(b.branch, bzr_branch.Branch))
        self.assertTrue(b.lp_branch.bzr_identity)
        self.assertFalse(b.has_tree)
        self.assertFalse(hasattr(b, 'tree'))

    def test_create_with_tree(self):
        '''Test the creation of a TarmacBranch with a created tree.'''
        b = branch.Branch(MockLPBranch(), create_tree=True)

        self.assertTrue(isinstance(b, branch.Branch))
        self.assertTrue(isinstance(b.branch, bzr_branch.Branch))
        self.assertTrue(b.lp_branch.bzr_identity)
        self.assertTrue(b.has_tree)
        self.assertTrue(hasattr(b, 'tree'))
