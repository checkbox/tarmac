'''Configuration handler.'''
from ConfigParser import SafeConfigParser as ConfigParser
import os

CONFIG_DIR = os.path.expanduser('~/.config/tarmac')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config')

def create_config_dirs():
    '''Create the configuration directory if it doesn't exist.'''
    if not os.path.exists(os.path.expanduser('~/.config')):
        os.mkdir(os.path.expanduser('~/.config'))
    if not os.path.exists(os.path.expanduser('~/.config/tarmac')):
        os.mkdir(os.path.expanduser('~/.config/tarmac'))
    if not os.path.exists(os.path.expanduser('~/.config/tarmac/cachedir')):
        os.mkdir(os.path.expanduser('~/.config/tarmac/cachedir'))

def get_config():
    '''Get the Configuration object.'''
    config = ConfigParser()
    config.read([CONFIG_FILE])
    try:
        config.write(open(CONFIG_FILE, 'wb'))
    except IOError:
        create_config_dirs()
        config.write(open(CONFIG_FILE, 'wb'))
    return config

