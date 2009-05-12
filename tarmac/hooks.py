# Copyright 2009 Paul Hummer - See LICENSE
'''Hooks for Tarmac.'''

from bzrlib import hooks


class TarmacHooks(hooks.Hooks):
    '''Hooks for Tarmac.'''

    def __init__(self):
        hooks.Hooks.__init__(self)
        self.create_hook(hooks.HookPoint('pre_tarmac_commit',
            'Called right after Tarmac checks out and merges in a new '
            'branch, but before committing.',
            (1, 14, 0), False))


        self.create_hook(hooks.HookPoint('merge_request_body',
            "Called with a MergeRequestBodyParams when a body is needed for"
            " a merge request.  Callbacks must return a body.  If more"
            " than one callback is registered, the output of one callback is"
            " provided to the next.", (1, 15, 0), False))


