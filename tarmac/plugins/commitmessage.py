# Copyright 2009 Paul Hummer - See LICENSE
'''Tarmac plugin for enforcing a commit message format.'''
from tarmac.hooks import tarmac_hooks
from tarmac.plugins import TarmacPlugin


class CommitMessageTemplate(TarmacPlugin):
    '''Tarmac plugin for modifying the commit message to adhere to a template.

    This plugin checks for a commit_message_template specific to the project.
    If to finds one, it will locally change the commit message to use the
    template.
    '''

    def __call__(self, options, configuration, candidate, trunk):
    # pylint: disable-msg=W0613

        if configuration.commit_message_template:
            self.template = configuration.commit_message_template
            self.template = self.template.replace('<', '%(').replace(
                '>', ')s')
        else:
            self.template = '%(commit_message)s'

        candidate.commit_message = self.template % {
            'author': candidate.source_branch.owner.display_name,
            'commit_message': candidate.commit_message,
            'reviewer': candidate.reviewer.display_name}

tarmac_hooks['pre_tarmac_commit'].hook(CommitMessageTemplate(),
    'Commit messsage template editor.')

