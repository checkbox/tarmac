'''Configuration handler.'''
from ConfigParser import SafeConfigParser as ConfigParser
import os


class TarmacConfig:
    '''A configuration class.'''

    def __init__(self, section=None):
        '''The config options are based on ~/.config/tarmac.

        If the configuration directories don't exist, they will be created.
        The section parameter is for coping with multiple projects in a single
        config.
        '''
        self.CONFIG_HOME = os.path.expanduser('~/.config/tarmac')
        self.CONFIG = os.path.join(self.CONFIG_HOME, 'config')
        self.CREDENTIALS = os.path.join(self.CONFIG_HOME, 'credentials')

        self._check_config_dirs()

    def _check_config_dirs(self):
        '''Create the configuration directory if it doesn't exist.'''
        if not os.path.exists(os.path.expanduser('~/.config')):
            os.mkdir(os.path.expanduser('~/.config'))
        if not os.path.exists(os.path.expanduser('~/.config/tarmac')):
            os.mkdir(os.path.expanduser('~/.config/tarmac'))
        if not os.path.exists(os.path.expanduser('~/.config/tarmac/cachedir')):
            os.mkdir(os.path.expanduser('~/.config/tarmac/cachedir'))


