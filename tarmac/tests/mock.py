# Copyright 2009 Paul Hummer - See LICENSE
'''Mock objects for Tarmac!'''
from base64 import b64encode
import math
import os
import tempfile

from bzrlib.branch import Branch
from bzrlib.bzrdir import BzrDir


class MockLPProject(object):
    '''A mock LP Project.'''

    def __init__(self):
        self.name = b64encode(os.urandom(int(math.ceil(0.75*10))),'-_')[:10]


class MockLPBranch(object):
    '''A mock LP Branch.'''

    def __init__(self, source_branch=None):
        self.temp_dir = tempfile.mkdtemp()
        if source_branch:
            bzrdir = source_branch.bzrdir.sprout(
                self.temp_dir)
            self._internal_tree, self._internal_bzr_branch = \
                    bzrdir.open_tree_or_branch(self.temp_dir)
        else:
            self._internal_bzr_branch = BzrDir.create_branch_convenience(
                self.temp_dir)
        self.bzr_identity = self._internal_bzr_branch.base
        self.project = MockLPProject()

