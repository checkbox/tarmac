# Copyright 2009 Paul Hummer - See LICENSE
'''Tarmac branch tools.'''
import os
import shutil
import tempfile

from bzrlib import branch as bzr_branch


class Branch(object):
    '''Wrapper for working with branches.

    This class wraps the Launchpad branch and the bzrlib branch functionalities
    to work seamlessly with both.
    '''

    def __init__(self, lp_branch, create_tree=False):

        self.has_tree = create_tree
        self.lp_branch = lp_branch
        self.branch = bzr_branch.Branch.open(self.lp_branch.bzr_identity)
        if self.has_tree:
            self._set_up_working_tree()

    def _set_up_working_tree(self):
        '''Create the dir and working tree.'''
        self.temporary_dir = os.path.join(tempfile.gettempdir(),
                                          self.lp_branch.project.name)
        if os.path.exists(self.temporary_dir):
            shutil.rmtree(self.temporary_dir)
        self.tree = self.branch.create_checkout(self.temporary_dir)

    def merge(self, branch):
        '''Merge from another tarmac.branch.Branch instance.'''
        if not self.has_tree:
            raise Exception('This branch wasn\'t set up to do merging,')
        self.tree.merge_from_branch(branch.branch)

    def cleanup(self):
        '''Remove the working tree from the temp dir.'''
        if self.has_tree:
            self._set_up_working_tree()

    def commit(self, commit_message):
        '''Commit changes.'''
        if not self.has_tree:
            raise Exception('This branch has no working tree.')
        self.tree.commit(commit_message)

    @property
    def landing_candidates(self):
        '''Wrap the LP representation of landing_candidates.'''
        return self.lp_branch.landing_candidates

