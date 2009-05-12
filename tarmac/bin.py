# Copyright 2009 Paul Hummer - See LICENSE
'''Code used by Tarmac scripts.'''
import atexit
import logging
from optparse import OptionParser
import os
from shutil import rmtree
import subprocess
import sys

from bzrlib import branch, bzrdir
from bzrlib.errors import PointlessMerge
from bzrlib.plugin import load_plugins
from launchpadlib.errors import HTTPError

from tarmac.config import TarmacConfig
from tarmac.hooks import TarmacHooks
from tarmac.utils import get_launchpad_object

load_plugins()


class TarmacScript:
    '''An abstract script for reusable parts of Tarmac.'''

    hooks = TarmacHooks()

    def __init__(self, test_mode=False):
        self.parser = self._create_option_parser()
        self.options, self.args = self.parser.parse_args()
        self.test_mode = test_mode

    def create_pid(self):
        '''Create a pidfile for the running process.'''
        assert not os.path.exists(self.configuration.PID_FILE)
        pidfile = open(self.configuration.PID_FILE, 'wb')
        pidfile.write(str(os.getpid()))
        pidfile.close()
        atexit.register(self.delete_pid)

    def delete_pid(self):
        '''Delete the pid file.

        This method is usually called when the atexit signal is emitted.
        '''
        assert os.path.exists(self.configuration.PID_FILE)
        os.remove(self.configuration.PID_FILE)

    def _create_option_parser(self):
        '''Create the option parser.'''
        raise NotImplementedError

    def main(self):
        '''Main part of each script.'''
        raise NotImplementedError


class TarmacLander(TarmacScript):
    '''Tarmac script.'''

    def __init__(self, test_mode=False):

        TarmacScript.__init__(self, test_mode)

        self.dry_run = self.options.dry_run

        if len(self.args) != 1:
            self.parser.error("Please specify a project name.")

        self.project, = self.args
        self.configuration = TarmacConfig(self.project)

        if self.options.test_command:
            self.test_command = self.options.test_command
        elif self.configuration.test_command:
            self.test_command = self.configuration.test_command
        else:
            self.test_command = None

        logging.basicConfig(filename=self.configuration.log_file,
            level=logging.INFO)
        self.logger = logging.getLogger('tarmac-lander')

        # Write a pid file
        if not test_mode:
            if os.path.exists(self.configuration.PID_FILE):
                message = 'An instance of tarmac is already running.'
                self.logger.info(message)
                print message
                sys.exit()
            self.create_pid()

    def _create_option_parser(self):
        '''See `TarmacScript._create_option_parser`.'''
        parser = OptionParser("%prog [options] <projectname>")
        parser.add_option('--dry-run', action='store_true',
            help='Merge the approved branch candidates (and optionally run '
                 'their accompanying test command), and then roll back the '
                 'trunk branch to pristine state.')
        parser.add_option('--test-command', type='string', default=None,
            metavar='TEST',
            help='The test command to run after merging a branch.')
        return parser

    def _get_reviewers(self, candidate):
        '''Get all reviewers who approved the review.'''
        return [comment.reviewer for comment in candidate.all_comments
            if comment.vote == u'Approve'].join(', ')

    def main(self):
        '''See `TarmacScript.main`.'''

        try:
            launchpad = get_launchpad_object(self.configuration)
        except HTTPError:
            message = (
                'Oops!  It appears that the OAuth token is invalid.  Please '
                'delete %(credential_file)s and re-authenticate.' %
                    {'credential_file': self.configuration.CREDENTIALS})
            self.logger.error(message)
            print message
            sys.exit()

        project = launchpad.projects[self.project]
        try:
            trunk = project.development_focus.branch
        except AttributeError:
            message = (
                'Oops!  It looks like you\'ve forgotten to specify a '
                'development focus branch.  Please link your "trunk" branch '
                'to the trunk development focus.')
            self.logger.error(message)
            print message
            sys.exit()

        candidates = [entry for entry in trunk.landing_candidates
                        if entry.queue_status == u'Approved']
        if not candidates:
            self.logger.info('No branches approved to land.')
            return

        temp_dir = os.path.join('/tmp', self.project)
        if os.path.exists(temp_dir):
            rmtree(temp_dir)
        os.mkdir(temp_dir)
        accelerator, target_branch = bzrdir.BzrDir.open_tree_or_branch(
            trunk.bzr_identity)
        target_tree = target_branch.create_checkout(
            temp_dir, None, True, accelerator)

        for candidate in candidates:

            if not candidate.commit_message:
                self.logger.error(
                    'Proposal to merge %(source_branch)s contains an empty '
                    'commit message.  Skipping.' % {
                        'source_branch': candidate.source_branch.bzr_identity})
                continue

            commit_dict = {}
            commit_dict['commit_line'] = candidate.commit_message
            # This is a great idea, but apparently reviewer isn't exposed
            # in the API just yet.
            #commit_dict['reviewers'] = self._get_reviewers(candidate)

            if self.configuration.commit_string:
                commit_string = self.configuration.commit_string
            else:
                commit_string = ('%(commit_line)s')
            commit_message = commit_string % commit_dict

            print '%(source_branch)s - %(commit_message)s' % {
                'source_branch': candidate.source_branch.bzr_identity,
                'commit_message': commit_message}

            source_branch = branch.Branch.open(
                candidate.source_branch.bzr_identity)

            try:
                target_tree.merge_from_branch(source_branch)
            except PointlessMerge:
                target_tree.revert()
                continue

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
                        print '  - Branch passed test command'
                else:
                    if self.dry_run:
                        print '  - Branch failed test command'
                    target_tree.revert()
                    comment = u'\n'.join([stdout_value, stderr_value])
                    candidate.createComment(subject="Failed test command",
                                            content=comment)
                    candidate.queue_status = u'Needs review'
                    candidate.lp_save()
            else:
                if not self.dry_run:
                    target_tree.commit(commit_message)
                else:
                    target_tree.revert()


