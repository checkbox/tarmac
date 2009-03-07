# Copyright (c) 2009 - Paul Hummer
'''Configuration handler.'''
# pylint: disable-msg=C0103
import os
from ConfigParser import NoSectionError
from ConfigParser import SafeConfigParser as ConfigParser


class TarmacConfig:
    '''A configuration class.'''

    def __init__(self, section=None):
        '''The config options are based on ~/.config/tarmac.

        If the configuration directories don't exist, they will be created.
        The section parameter is for coping with multiple projects in a single
        config.
        '''
        self.CONFIG_HOME = os.path.expanduser('~/.config/tarmac')
        self.CREDENTIALS = os.path.join(self.CONFIG_HOME, 'credentials')

        self.CACHEDIR = os.path.join(self.CONFIG_HOME, 'cachedir')

        self._check_config_dirs()
        self._CONFIG_FILE = os.path.join(self.CONFIG_HOME, 'tarmac.conf')
        self._CONFIG = ConfigParser()
        self._CONFIG.read(self._CONFIG_FILE)
        self._SECTION = section

    def _check_config_dirs(self):
        '''Create the configuration directory if it doesn't exist.'''
        if not os.path.exists(os.path.expanduser('~/.config')):
            os.mkdir(os.path.expanduser('~/.config'))
        if not os.path.exists(os.path.expanduser('~/.config/tarmac')):
            os.mkdir(os.path.expanduser('~/.config/tarmac'))
        if not os.path.exists(os.path.expanduser('~/.config/tarmac/cachedir')):
            os.mkdir(os.path.expanduser('~/.config/tarmac/cachedir'))

    def get(self, key):
        '''Get a config value for the given key.'''
        try:
            return self._CONFIG.get(self._SECTION, key);
        except (NoOptionError, NoSectionError):
            return None


