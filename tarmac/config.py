# Copyright 2009 Paul Hummer - See LICENSE
'''Configuration handler.'''
# pylint: disable-msg=C0103
import os
import sys
from ConfigParser import NoSectionError, NoOptionError
from ConfigParser import SafeConfigParser as ConfigParser


class TarmacConfig:
    '''A configuration class.'''

    def __init__(self, project=None):
        '''The config options are based on ~/.config/tarmac.

        If the configuration directories don't exist, they will be created.
        The section parameter is for coping with multiple projects in a single
        config.
        '''
        if sys.platform == 'win32':
            from bzrlib import win32utils
            # This is for settings that stay permanent, and should "Roam"
            appdata = win32utils.get_appdata_location_unicode()
            self.CONFIG_HOME = os.path.join(appdata, 'Tarmac', '1.0')
            # These are for settings that should *not* "Roam"
            local_appdata = win32utils.get_local_appdata_location()
            pid_base = os.path.join(local_appdata, 'Tarmac', '1.0')
            self.PID_FILE = os.path.join(pid_base, str(project))
        else:
            self.CONFIG_HOME = os.path.expanduser('~/.config/tarmac')
            self.PID_FILE = '/var/tmp/tarmac-%(project)s' % {'project': project }

        self.CREDENTIALS = os.path.join(self.CONFIG_HOME, 'credentials')

        self.CACHEDIR = os.path.join(self.CONFIG_HOME, 'cachedir')

        self._check_config_dirs()
        self._CONFIG_FILE = os.path.join(self.CONFIG_HOME, 'tarmac.conf')
        self._CONFIG = ConfigParser()
        self._CONFIG.read(self._CONFIG_FILE)
        self._PROJECT = project

    def _check_config_dirs(self):
        '''Create the configuration directory if it doesn't exist.'''
        if not os.path.exists(self.CONFIG_HOME):
            os.makedirs(self.CONFIG_HOME)
        if not os.path.exists(self.CACHEDIR):
            os.makedirs(self.CACHEDIR)
        pid_dir = os.path.dirname(self.PID_FILE)
        if not os.path.exists(pid_dir):
            os.makedirs(pid_dir)

    @property
    def commit_message_template(self):
        '''Return the commit_message_template.'''
        return self.get('commit_message_template')

    @property
    def test_command(self):
        '''Get the test_command from the stored config.'''
        return self.get('test_command')

    @property
    def cia_server(self):
        '''Server for the CIA plugin.'''
        return self.get('cia_server')

    @property
    def cia_project(self):
        '''Project for the CIA plugin.'''
        return self.get('cia_project')

    @property
    def log_file(self):
        '''Get the log_file from config or return a default.'''
        try:
            return self._CONFIG.get(self._PROJECT, 'log_file')
        except (NoOptionError, NoSectionError):
            return os.path.join(self.CONFIG_HOME, self._PROJECT)

    def get(self, key):
        '''Get a config value for the given key.'''
        try:
            return self._CONFIG.get(self._PROJECT, key)
        except (NoOptionError, NoSectionError):
            return None

