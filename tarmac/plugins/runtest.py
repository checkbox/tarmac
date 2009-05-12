# Copyright 2009 Paul Hummer - See LICENSE
'''Tarmac plugin for running tests pre-commit.'''

from tarmac.plugins import TarmacPlugin


class RunTest(TarmacPlugin):
    '''Tarmac plugin for running a test command.

    This plugin checks for a config setting specific to the project.  If it
    finds one, it will run that command pre-commit.  On fail, it calls the
    do_failed method, and on success, continues.
    '''
    #TODO: Add the specific config it checks for.
    #TODO: Add the ability to override the test command in the command line.

    def __call__(self, test_command=None):
        pass

    def do_failed(self):
        '''Perform failure tests.

        In this case, the output of the test command is posted as a comment,
        and the merge proposal is then set to "Needs review" so that Tarmac
        doesn't attempt to merge it again without human interaction.  An
        exception is then raised to prevent the commit from happening.
        '''

