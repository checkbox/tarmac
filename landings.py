import os

from launchpadlib.launchpad import Credentials, Launchpad, EDGE_SERVICE_ROOT

from tarmac import config

configuration = config.get_config()

#LOGIN_CREDENTIALS = os.path.abspath('~/.config/tarmac/login-credentials')
#CACHEDIR = os.path.abspath('~/.config/tarmac/cache')

#if not os.path.exists(CACHEDIR):
#    os.mkdir(CACHEDIR)

#if os.path.exists(LOGIN_CREDENTIALS):
#    credentials = Credentials()
#    credentials.load(open(LOGIN_CREDENTIALS))
#    launchpad = Launchpad(credentials, STAGING_SERVICE_ROOT, CACHEDIR)
#else:
#    launchpad = Launchpad.get_token_and_login('Tarmac',
#        STAGING_SERVICE_ROOT, cachedir)
#    launchpad.credentials.save(file(LOGIN_CREDENTIALS, 'w'))


