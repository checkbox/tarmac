'''Plugin utilities for Tarmac.'''
# pylint: disable-msg=W0122,W0612

import imp
import os

from tarmac import plugins as _mod_plugins

# XXX: rockstar - There should be a way to load from ENV as well.
TARMAC_PLUGIN_PATHS = [
    os.path.expanduser('~/.config/tarmac/plugins'),
    os.path.join(os.path.dirname(__file__), 'plugins')]

def load_plugins():
    '''Load the plugins for Tarmac.'''

    valid_suffixes = [suffix for suffix, mod_type, flags in imp.get_suffixes()
        if flags in (imp.PY_SOURCE, imp.PY_COMPILED)]
    package_entries = ['__init__' + suffix for suffix in valid_suffixes]

    plugin_names = set()
    for path in TARMAC_PLUGIN_PATHS:
        try:
            for _file in os.listdir(path):
                full_path = os.path.join(path, _file)
                if os.path.isdir(full_path):
                    for entry in package_entries:
                        if os.path.isfile(os.path.join(full_path, entry)):
                            # This directory is definitely a package
                            break
                        else:
                            continue

                else:
                    if _file.startswith('.'):
                        continue # Hidden file, should be ignored.
                    for suffix_info in imp.get_suffixes():
                        if _file.endswith(suffix_info[0]):
                            _file = _file[:-len(suffix_info[0])]
                            if (suffix_info[2] == imp.C_EXTENSION and
                                                    _file.endswith('module')):
                                _file = _file[:-len('module')]
                            break
                        else:
                            continue

                if _file == '__init__':
                    continue
                elif getattr(_mod_plugins, _file, None):
                    continue # Plugin is already loaded.
                else:
                    plugin_names.add(_file)
        except OSError: # Usually the dir does not exist
            continue

    for name in plugin_names:
        try:
            exec 'import tarmac.plugins.%s' % name in {}
        except KeyboardInterrupt:
            raise

