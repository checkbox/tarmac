# Copyright 2009 Paul Hummer - See LICENSE
'''Hooks for Tarmac.'''

from bzrlib import hooks


class TarmacHookPoint(hooks.HookPoint):
    '''A special HookPoint for Tarmac.

    This HookPoint implements a fire method that the bzrlib.hooks.HookPoint
    doesn't have.  If this turns out to be helpful, than a patch to Bazaar
    should be made to implement it in Bazaar.
    '''

    def fire(self, *args, **kwargs):
        '''Fire all registered hooks for self.'''
        for hook in self:
            hook(*args, **kwargs)


class TarmacHookRegistry(hooks.Hooks):
    '''Hooks for Tarmac.'''

    def __init__(self):
        hooks.Hooks.__init__(self)

        self.create_hook(TarmacHookPoint('pre_tarmac_commit',
            'Called right after Tarmac checks out and merges in a new '
            'branch, but before committing.',
            (1, 14, 0), False))

        self.create_hook(TarmacHookPoint('post_tarmac_commit',
            'Called right after Tarmac commits the merged revision',
            (1, 14, 0), False))


tarmac_hooks = TarmacHookRegistry()

