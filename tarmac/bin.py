# Copyright (c) 2009 - Paul Hummer
'''Code used by Tarmac scripts.'''
from optparse import OptionParser
import os
import sys

from bzrlib import branch, bzrdir
from bzrlib.plugin import load_plugins
from launchpadlib.errors import HTTPError

from tarmac.config import TarmacConfig
from tarmac.exceptions import NoCommitMessage
from tarmac.utils import get_launchpad_object

load_plugins()
DEV_SERVICE_ROOT = 'https://api.launchpad.dev/beta/'


class TarmacLander:
    '''Tarmac script.'''

    def __init__(self):

        parser = OptionParser("%prog [options] <projectname>")
        parser.add_option('--dry-run', action='store_true', dest='dry_run',
            help='Print out the branches that would be merged and their '
                 'commit messages, but don\'t actually merge the branches.')
        options, args = parser.parse_args()
        self.dry_run = options.dry_run

        if len(args) != 1:
            # This code is merely a placeholder until I can get proper argument
            # handling, at which point this should print usage information.
            parser.error("Please specify a project name.")

        self.project, = args

    def _find_commit_message(self, comments):
        '''Find the proper commit comment.'''
        for comment in comments:
            if comment.title.lower().startswith('commit message'):
                return comment.message_body
            elif comment.message_body.lower().startswith('commit message: '):
                return comment.message_body[len('Commit message: '):]
        raise NoCommitMessage

    def main(self):
        configuration = TarmacConfig()

        try:
            launchpad = get_launchpad_object(configuration)
        except HTTPError:
            print (
                'Oops!  It appears that the OAuth token is invalid.  Please '
                'delete %(credential_file)s and re-authenticate.' %
                    {'credential_file': configuration.CREDENTIALS})
            sys.exit()

        project = launchpad.projects[self.project]
        try:
            trunk = project.development_focus.branch
        except AttributeError:
            print (
                'Oops!  It looks like you\'ve forgotten to specify a '
                'development focus branch.  Please link your "trunk" branch '
                'to the trunk development focus.')
            sys.exit()

        candidates = [entry for entry in trunk.landing_candidates
                        if entry.queue_status == u'Approved']

        for candidate in candidates:

            commit_message = self._find_commit_message(candidate.all_comments)
            if self.dry_run:
                print '%(source_branch)s - %(commit_message)s' % {
                    'source_branch': candidate.source_branch.bzr_identity,
                    'commit_message': commit_message}
                continue

            temp_dir = '/tmp/merge-%(source)s-%(pid)s' % {
                'source': candidate.source_branch.name,
                'pid': os.getpid()
                }
            os.mkdir(temp_dir)

            accelerator, target_branch = bzrdir.BzrDir.open_tree_or_branch(
                candidate.target_branch.bzr_identity)
            target_tree = target_branch.create_checkout(
                temp_dir, None, True, accelerator)
            source_branch = branch.Branch.open(
                candidate.source_branch.bzr_identity)

            target_tree.merge_from_branch(source_branch)
            # TODO: Add hook code.
            target_tree.commit(candidate.all_comments[0].message_body)


