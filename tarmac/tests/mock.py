# Copyright 2009 Paul Hummer - See LICENSE
'''Mock objects for Tarmac!'''
from base64 import b64encode
import math
import os
import tempfile

from bzrlib import bzrdir


class MockLPProject(object):
    '''A mock LP Project.'''

    def __init__(self):
        self.name = b64encode(os.urandom(int(math.ceil(0.75*10))),'-_')[:10]


class MockLPBranch(object):
    '''A mock LP Branch.'''

    def __init__(self):
        temp_dir = tempfile.mkdtemp()
        self._internal_bzr_branch = bzrdir.BzrDir.create_branch_convenience(
            temp_dir)
        self.bzr_identity = self._internal_bzr_branch.base
        self.project = MockLPProject()

