'''Bazaar Plugin for Tarmac.'''

from bzrlib.lazy_import import lazy_import
lazy_import(globals(), '''
from bzrlib.hooks import known_hooks

''')

known_hooks.register_lazy(
    ('tarmac.hooks.TarmacHooks', 'TarmacLander.hooks'),
    'tarmac.hooks', 'TarmacHooks')

