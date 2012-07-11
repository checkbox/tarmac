'''Tests for tarmac.bin.commands.py.'''
from cStringIO import StringIO
import os
import shutil
import sys

from tarmac.bin import commands
from tarmac.bin.registry import CommandRegistry
from tarmac.branch import Branch
from tarmac.config import TarmacConfig
from tarmac.exceptions import UnapprovedChanges
from tarmac.tests import TarmacTestCase, BranchTestCase
from tarmac.tests.mock import MockLPBranch, Thing


class FakeCommand(commands.TarmacCommand):
    '''Fake command for testing.'''

    def get_help_text(self):
        return 'You need help.\n'

    def run(self, *args, **kwargs):
        return


class TestCommand(TarmacTestCase):
    '''Test for tarmac.bin.commands.Command.'''

    def test__init__(self):
        registry = CommandRegistry(config=self.config)
        command_name = u'test'
        command = commands.TarmacCommand(registry)
        command.NAME = command_name
        self.assertEqual(command.NAME, command_name)
        self.assertTrue(isinstance(command.config, TarmacConfig))

    def test_run(self):
        registry = CommandRegistry(config=self.config)
        command = commands.TarmacCommand(registry)
        command.run()


class TestAuthCommand(TarmacTestCase):
    '''Test for tarmac.bin.command.cmd_auth.'''

    # XXX: rockstar - 10 Jan 2010 - How do I test this with the OAuth request,
    # etc?
    #def test_run(self):
    #    '''Test that calling the auth command gets a Lanuchpad token.'''

    #    tmp_stdout = StringIO()
    #    old_stdout = sys.stdout
    #    sys.stdout = tmp_stdout

    #    command = cmd_auth()
    #    self.assertFalse(os.path.exists(command.config.CREDENTIALS))
    #    command.run()
    #    self.assertEqual(tmp_stdout.getvalue(), '')

    #    sys.stdout = old_stdout

    def test_run_already_authenticated(self):
        '''If the user has already been authenticated, do not try again.'''
        registry = CommandRegistry(config=self.config)
        registry.register_command('authenticate', commands.cmd_authenticate)
        command = registry._get_command(commands.cmd_authenticate,
                                        'authenticate')

        def fail_if_get_lp_object(*args, **kwargs):
            '''Fail if get_launchpad_object is called here.'''
            raise Exception('Not already authenticated.')

        command.get_launchpad_object = fail_if_get_lp_object
        command.run()


class TestHelpCommand(TarmacTestCase):

    def test_run(self):
        tmp_stdout = StringIO()
        old_stdout = sys.stdout
        sys.stdout = tmp_stdout

        registry = CommandRegistry(config=self.config)
        registry.register_command('foo', FakeCommand)

        registry.register_command('help', commands.cmd_help)
        command = registry._get_command(commands.cmd_help, 'help')
        command.outf = tmp_stdout
        command.run(command='foo')
        self.assertEqual(
            tmp_stdout.getvalue(),
            'You need help.\n')

        sys.stdout = old_stdout


class TestMergeCommand(BranchTestCase):

    def setUp(self):
        super(TestMergeCommand, self).setUp()

        self.branches = [Thing(
                bzr_identity=self.branch2.lp_branch.bzr_identity,
                display_name=self.branch2.lp_branch.bzr_identity,
                name='source',
                revision_count=self.branch2.lp_branch.revision_count,
                landing_candidates=[]),
                         Thing(
                bzr_identity=self.branch1.lp_branch.bzr_identity,
                display_name=self.branch1.lp_branch.bzr_identity,
                name='target',
                revision_count=self.branch1.lp_branch.revision_count,
                landing_candidates=None)]
        self.proposals = [Thing(
                self_link=u'http://api.edge.launchpad.net/devel/proposal0',
                queue_status=u'Needs Review',
                commit_message=u'Commitable.',
                source_branch=self.branches[0],
                target_branch=self.branches[1],
                prerequisite_branch=None,
                createComment=self.createComment,
                setStatus=self.lp_save,
                lp_save=self.lp_save,
                reviewed_revid=None,
                votes=[Thing(
                        comment=Thing(vote=u'Needs Fixing'),
                        reviewer=Thing(display_name=u'Reviewer'))]),
                          Thing(
                self_link=u'https://api.launchpad.net/1.0/proposal1',
                queue_status=u'Approved',
                commit_message=u'Commit this.',
                source_branch=self.branches[0],
                target_branch=self.branches[1],
                prerequisite_branch=None,
                createComment=self.createComment,
                setStatus=self.lp_save,
                lp_save=self.lp_save,
                reviewed_revid=None,
                votes=[Thing(
                        comment=Thing(vote=u'Approve'),
                        reviewer=Thing(display_name=u'Reviewer')),
                                       Thing(
                        comment=Thing(vote=u'Abstain'),
                        reviewer=Thing(display_name=u'Reviewer2'))])]
        self.branches[1].landing_candidates = self.proposals

        self.launchpad = Thing(branches=Thing(getByUrl=self.getBranchByUrl))
        self.error = None
        registry = CommandRegistry(config=self.config)
        registry.register_command('merge', commands.cmd_merge)

        self.command = registry._get_command(commands.cmd_merge, 'merge')

    def lp_save(self, *args, **kwargs):
        """Do nothing here."""
        pass

    def createComment(self, subject=None, content=None):
        """Fake createComment method for proposals."""
        self.error = UnapprovedChanges(subject, content)

    def getBranchByUrl(self, url=None):
        """Fake method to get branches matching a URL."""
        try:
            return [x for x in self.branches if x.bzr_identity == url][0]
        except IndexError:
            return None

    def test_run(self):
        """Test that the merge command merges a branch successfully."""
        self.proposals[1].reviewed_revid = \
            self.branch2.bzr_branch.last_revision()
        self.command.run(launchpad=self.launchpad)

    def test_run_unapprovedchanges(self):
        """Test that a mismatch between approved and tip raises an error."""
        self.proposals[1].reviewed_revid = \
            self.branch2.bzr_branch.dotted_revno_to_revision_id(
            (self.branch2.bzr_branch.revno() - 1,))
        self.command.run(launchpad=self.launchpad)
        self.assertTrue(isinstance(self.error, UnapprovedChanges))

    def test_run_no_reviewed_revid(self):
        """Test that no reviewed revid raises an error."""
        self.proposals[1].reviewed_revid = None
        self.command.run(launchpad=self.launchpad)
        self.assertTrue(isinstance(self.error, UnapprovedChanges))
        self.assertEqual(self.error.comment,
                         u'No approved revision specified.')

    def test_get_reviews(self):
        """Test that the _get_reviews method gives the right lists."""
        self.assertEqual(self.command._get_reviews(self.proposals[0]),
                         [u'Reviewer;Needs Fixing'])
        self.assertEqual(self.command._get_reviews(self.proposals[1]),
                         [u'Reviewer;Approve', u'Reviewer2;Abstain'])

    def test_run_merge_url_substitution(self):
        """Test that the merge urls get substituted correctly."""
        self.proposals[1].reviewed_revid = \
            self.branch2.bzr_branch.last_revision()
        self.command.run(launchpad=self.launchpad)
        revid = self.branch1.bzr_branch.last_revision()
        last_rev = self.branch1.bzr_branch.repository.get_revision(revid)
        self.assertEqual(last_rev.properties.get('merge_url', None),
                         u'http://code.launchpad.net/proposal1')

        # This proposal merged ok
        self.proposals[1].queue_status = u'Merged'

        # Make a new commit, approve the propsoal, merge, and verify
        self.branch2.commit('New commit to merge.')
        self.proposals[0].queue_status = u'Approved'
        self.proposals[0].reviewed_revid = \
            self.branch2.bzr_branch.last_revision()
        self.command.run(launchpad=self.launchpad)
        revid = self.branch1.bzr_branch.last_revision()
        last_rev = self.branch1.bzr_branch.repository.get_revision(revid)
        self.assertEqual(last_rev.properties.get('merge_url', None),
                         u'http://code.launchpad.net/proposal0')

    def test_run_merge_with_unmerged_prerequisite_fails(self):
        """Test that mereging a branch with an unmerged prerequisite fails."""
        # Create a 3rd prerequisite branch we'll use to test with
        branch3_dir = os.path.join(self.TEST_ROOT, 'branch3')
        mock3 = MockLPBranch(branch3_dir, source_branch=self.branch1.lp_branch)
        branch3 = Branch.create(mock3, self.config, create_tree=True,
                                target=self.branch1)
        branch3.commit('Prerequisite commit.')
        branch3.lp_branch.revision_count += 1

        # Merge the prerequisite and create another commit after
        self.branch2.merge(branch3)
        self.branch2.commit('Merged prerequisite.')
        self.branch2.commit('Post-merge commit.')
        self.branch2.lp_branch.revision_count += 2

        # Set up an unapproved proposal for the prerequisite
        branch3.lp_branch.display_name = branch3.lp_branch.bzr_identity
        branch3.lp_branch.name = 'branch3'
        branch3.lp_branch.landing_candidates = []
        b3_proposal = Thing(
            self_link=u'http://api.edge.launchpad.net/devel/proposal3',
            queue_status=u'Work in Progress',
            commit_message=u'Commitable.',
            source_branch=branch3.lp_branch,
            target_branch=self.branches[1],
            prerequisite_branch=None,
            createComment=self.createComment,
            setStatus=self.lp_save,
            lp_save=self.lp_save,
            reviewed_revid=None,
            votes=[Thing(
                    comment=Thing(vote=u'Needs Fixing'),
                    reviewer=Thing(display_name=u'Reviewer'))])

        branch3.lp_branch.landing_targets = [b3_proposal]

        self.proposals.append(b3_proposal)
        self.proposals[1].prerequisite_branch = branch3.lp_branch
        self.proposals[1].reviewed_revid = \
            self.branch2.bzr_branch.last_revision()
        self.command.run(launchpad=self.launchpad)
        shutil.rmtree(branch3_dir)
        self.assertEqual(self.error.comment,
                         u'The prerequisite lp:branch3 has not yet been '
                         u'merged into lp:branch1.')

    def test_run_merge_with_unproposed_prerequisite_fails(self):
        """Test that mereging a branch with an unmerged prerequisite fails."""
        # Create a 3rd prerequisite branch we'll use to test with
        branch3_dir = os.path.join(self.TEST_ROOT, 'branch3')
        mock3 = MockLPBranch(branch3_dir, source_branch=self.branch1.lp_branch)
        branch3 = Branch.create(mock3, self.config, create_tree=True,
                                target=self.branch1)
        branch3.commit('Prerequisite commit.')
        branch3.lp_branch.revision_count += 1

        # Merge the prerequisite and create another commit after
        self.branch2.merge(branch3)
        self.branch2.commit('Merged prerequisite.')
        self.branch2.commit('Post-merge commit.')
        self.branch2.lp_branch.revision_count += 2

        # Set up an unapproved proposal for the prerequisite
        branch3.lp_branch.display_name = branch3.lp_branch.bzr_identity
        branch3.lp_branch.name = 'branch3'
        branch3.lp_branch.landing_candidates = []
        b3_proposal = Thing(
            self_link=u'http://api.edge.launchpad.net/devel/proposal3',
            queue_status=u'Work in Progress',
            commit_message=u'Commitable.',
            source_branch=branch3.lp_branch,
            target_branch=self.branches[1],
            prerequisite_branch=None,
            createComment=self.createComment,
            setStatus=self.lp_save,
            lp_save=self.lp_save,
            reviewed_revid=None,
            votes=[Thing(
                    comment=Thing(vote=u'Needs Fixing'),
                    reviewer=Thing(display_name=u'Reviewer'))])

        branch3.lp_branch.landing_targets = []

        self.proposals.append(b3_proposal)
        self.proposals[1].prerequisite_branch = branch3.lp_branch
        self.proposals[1].reviewed_revid = \
            self.branch2.bzr_branch.last_revision()
        self.command.run(launchpad=self.launchpad)
        shutil.rmtree(branch3_dir)
        self.assertEqual(self.error.comment,
                         u'No proposals found for merge of lp:branch3 '
                         u'into lp:branch1.')

    def test_run_merge_with_prerequisite_with_multiple_proposals_fails(self):
        """Test that mereging a branch with an unmerged prerequisite fails."""
        # Create a 3rd prerequisite branch we'll use to test with
        branch3_dir = os.path.join(self.TEST_ROOT, 'branch3')
        mock3 = MockLPBranch(branch3_dir, source_branch=self.branch1.lp_branch)
        branch3 = Branch.create(mock3, self.config, create_tree=True,
                                target=self.branch1)
        branch3.commit('Prerequisite commit.')
        branch3.lp_branch.revision_count += 1

        # Merge the prerequisite and create another commit after
        self.branch2.merge(branch3)
        self.branch2.commit('Merged prerequisite.')
        self.branch2.commit('Post-merge commit.')
        self.branch2.lp_branch.revision_count += 2

        # Set up an unapproved proposal for the prerequisite
        branch3.lp_branch.display_name = branch3.lp_branch.bzr_identity
        branch3.lp_branch.name = 'branch3'
        branch3.lp_branch.landing_candidates = []
        b3_proposal = Thing(
            self_link=u'http://api.edge.launchpad.net/devel/proposal3',
            queue_status=u'Work in Progress',
            commit_message=u'Commitable.',
            source_branch=branch3.lp_branch,
            target_branch=self.branches[1],
            prerequisite_branch=None,
            createComment=self.createComment,
            setStatus=self.lp_save,
            lp_save=self.lp_save,
            reviewed_revid=None,
            votes=[Thing(
                    comment=Thing(vote=u'Needs Fixing'),
                    reviewer=Thing(display_name=u'Reviewer'))])

        branch3.lp_branch.landing_targets = [
            b3_proposal,
            Thing(
                target_branch=self.branches[1],
                queue_status='Needs Review')]

        self.proposals.append(b3_proposal)
        self.proposals[1].prerequisite_branch = branch3.lp_branch
        self.proposals[1].reviewed_revid = \
            self.branch2.bzr_branch.last_revision()
        self.command.run(launchpad=self.launchpad)
        shutil.rmtree(branch3_dir)
        self.assertEqual(self.error.comment,
                         u'More than one proposal found for merge of '
                         u'lp:branch3 into lp:branch1, which is not '
                         u'Superseded.')
