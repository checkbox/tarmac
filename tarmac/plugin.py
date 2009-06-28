'''Plugin utilities for Tarmac.'''

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
            for file in os.listdir(path):
                full_path = os.path.join(path, file)
                if os.path.isdir(full_path):
                    for entry in package_entries:
                        if os.path.isfile(os.path.join(full_path, entry)):
                            # This directory is definitely a package
                            break
                        else:
                            continue

                else:
                    if file.startswith('.'):
                        continue # Hidden file, should be ignored.
                    for suffix_info in imp.get_suffixes():
                        if file.endswith(suffix_info[0]):
                            file = file[:-len(suffix_info[0])]
                            if suffix_info[2] == imp.C_EXTENSION and file.endswith('module'):
                                file = file[:-len('module')]
                            break
                        else:
                            continue

                if file == '__init__':
                    continue
                elif getattr(_mod_plugins, file, None):
                    continue # Plugin is already loaded.
                else:
                    plugin_names.add(file)
        except OSError: # Usually the dir does not exist
            continue

    for name in plugin_names:
        try:
            exec 'import tarmac.plugins.%s' % name in {}
        except KeyboardInterrupt:
            raise

def load_plugin_from_dir(directory):
    '''Load a plugin from the dir.'''

def load_plugin_from_file(file):
    '''Load a plugin from a file.'''

