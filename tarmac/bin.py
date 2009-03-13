# Copyright (c) 2009 - Paul Hummer
'''Code used by Tarmac scripts.'''
from optparse import OptionParser
import os
import subprocess
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
        parser.add_option('--dry-run', action='store_true',
            help='Print out the branches that would be merged and their '
                 'commit messages, but don\'t actually merge the branches.')
        parser.add_option('--test-command', type='string', default=None,
            metavar='TEST',
            help='The test command to run after merging a branch.')
        options, args = parser.parse_args()
        self.dry_run = options.dry_run

        if len(args) != 1:
            parser.error("Please specify a project name.")

        self.project, = args
        self.configuration = TarmacConfig(self.project)

        if options.test_command:
            self.test_command = options.test_command
        elif self.configuration.test_command:
            self.test_command = self.configuration.test_command
        else:
            self.test_command = None

    def _find_commit_message(self, candidate):
        '''Find the proper commit comment.'''
        for comment in candidate.all_comments:
            try:
                if comment.title.lower().startswith('commit message'):
                    return comment.message_body
                elif comment.message_body.lower().startswith(
                                                        'commit message: '):
                    return comment.message_body[len('Commit message: '):]
            except AttributeError:
                continue
        raise NoCommitMessage

    def main(self):
        '''Execute the script.'''

        try:
            launchpad = get_launchpad_object(self.configuration)
        except HTTPError:
            print (
                'Oops!  It appears that the OAuth token is invalid.  Please '
                'delete %(credential_file)s and re-authenticate.' %
                    {'credential_file': self.configuration.CREDENTIALS})
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

            try:
                commit_dict = {}
                commit_dict['commit_line'] = self._find_commit_message(
                    candidate)
                # This is a great idea, but apparently reviewer isn't exposed
                # in the API just yet.
                #commit_dict['reviewers'] = self._get_reviewers(candidate)

                if self.configuration.commit_string:
                    commit_string = self.configuration.commit_string
                else:
                    commit_string = ('%(commit_line)s')
                commit_message = commit_string % commit_dict
            except NoCommitMessage:
                print ('Proposal to merge %(branch_name)s is missing '
                    'an associated commit message.  As a result, '
                    'the branch will not be merged.' % {
                    'branch_name': candidate.source_branch.bzr_identity})
                print
                continue


            if self.dry_run:
                print '%(source_branch)s - %(commit_message)s' % {
                    'source_branch': candidate.source_branch.bzr_identity,
                    'commit_message': commit_message}

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
            if self.test_command:
                cwd = os.getcwd()
                os.chdir(temp_dir)
                proc = subprocess.Popen(self.test_command,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                stdout_value, stderr_value = proc.communicate()
                retcode = proc.wait()
                os.chdir(cwd)
                if retcode == 0:
                    if not self.dry_run:
                        target_tree.commit(commit_message)
                    else:
                        print 'Branch passed test command'
                else:
                    if self.dry_run:
                        print 'Branch failed test command'
                    target_tree.revert()
                    comment = '\n'.join(['Branch failed test command',
                        stdout_value, stderr_value])
                    candidate.createComment(subject="unused", content=comment,
                                            vote='Needs Fixing')
                    candidate.queue_status = 'Needs Fixing'
                    candidate.lp_save()
            else:
                if not self.dry_run:
                    target_tree.commit(commit_message)

    def _get_reviewers(self, candidate):
        '''Get all reviewers who approved the review.'''
        return [comment.reviewer for comment in candidate.all_comments
            if comment.vote == u'Approve'].join(', ')

