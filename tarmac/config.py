'''Configuration handler.'''
from ConfigParser import SafeConfigParser as ConfigParser
import os


CONFIG_DIR = os,path.expanduser('~/.config/tarmac')

def create_config_dirs():
    '''Create the configuration directory if it doesn't exist.'''
    if not os.path.exists(os.path.expanduser('~/.config'):
        os.mkdir(os.path.expanduser('~/.config')
    if not os.path.exists(os.path.expanduser('~/.config/tarmac'):
        os.mkdir(os.path.expanduser('~/.config/tarmac')
    if not os.path.exists(os.path.expanduser('~/.config/tarmac/config'):
        os.mkdir(os.path.expanduser('~/.config/tarmac/config')

def get_config():
    '''Get the Configuration object.'''
    config = ConfigParser()
    config.read([os.path.join(CONFIG_DIR, 'config')])
    return config

