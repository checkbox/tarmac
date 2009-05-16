# Copyright 2009 Paul Hummer - See LICENSE
'''Tarmac branch tools.'''
import os
import shutil

from bzrlib import branch


class Branch(object):
    '''Wrapper for working with branches.

    This class wraps the Launchpad branch and the bzrlib branch functionalities
    to work seamlessly with both.
    '''

    def __init__(self, lp_branch, create_tree=False):

        self.has_tree = create_tree
        self.lp_branch = lp_branch
        self.branch = branch.Branch.open(self.lp_branch.bzr_identity)
        if create_tree:
            self.temporary_dir = os.path.join(
                '/tmp', self.lp_branch.project.name)
            self.tree = self.branch.create_checkout(self.temporary_dir)

    def merge(self, branch):
        '''Merge from another tarmac.branch.Branch instance.'''
        if not self.has_tree:
            raise Exception('This branch wasn\'t set up to do merging,')
        self.tree.merge_from_branch(branch.branch)

    def cleanup(self):
        '''Remove the working tree from the temp dir.'''
        if self.has_tree:
            shutil.rmtree(self.temporary_dir)

