# Copyright 2009 Paul Hummer - See LICENSE
'''Tarmac branch tools.'''
import os
import shutil

from bzrlib import branch, revision


class Branch(object):
    '''Wrapper for working with branches.

    This class wraps the Launchpad branch and the bzrlib branch functionalities
    to work seamlessly with both.
    '''

    def __init__(self, lp_branch, create_tree=False):

        self.has_tree = create_tree
        self.lp_branch = lp_branch
        self.author_list = None
        self.branch = branch.Branch.open(self.lp_branch.bzr_identity)
        if self.has_tree:
            self._set_up_working_tree()

    def _set_up_working_tree(self):
        '''Create the dir and working tree.'''
        temporary_dir = os.path.join('/tmp', self.lp_branch.project.name)
        if os.path.exists(temporary_dir):
            shutil.rmtree(temporary_dir)
        self.tree = self.branch.create_checkout(temporary_dir)
        if not self.author_list:
            self._set_authors()

    def _set_authors(self):
        '''Get the authors from the last revision and use it.'''
        # XXX Need to get all authors from revisions not in target
        last_rev = self.branch.last_revision()
        # If the list is None we need to make it empty first
        if not self.author_list:
            self.author_list = []
        # Only query for authors if last_rev is not null:
        if last_rev != 'null:':
            rev = self.branch.repository.get_revision(last_rev)
            self.author_list.append(rev.get_apparent_authors()[0])

    def merge(self, branch):
        '''Merge from another tarmac.branch.Branch instance.'''
        if not self.has_tree:
            raise Exception('This branch wasn\'t set up to do merging,')
        self.tree.merge_from_branch(branch.branch)

    def cleanup(self):
        '''Remove the working tree from the temp dir.'''
        if self.has_tree:
            self._set_up_working_tree()

    def commit(self, commit_message, authors=None):
        '''Commit changes.'''
        if not self.has_tree:
            raise Exception('This branch has no working tree.')
        if not authors:
            authors = self.authors
        self.tree.commit(commit_message, committer='Tarmac', authors=authors)

    @property
    def landing_candidates(self):
        return self.lp_branch.landing_candidates

    @property
    def authors(self):
        return self.author_list
