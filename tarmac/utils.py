# Copyright 2009 Paul Hummer - See LICENSE
'''Utilities for Tarmac, mostly dealing with Launchpad.'''
import os

from launchpadlib.launchpad import (Credentials, Launchpad, EDGE_SERVICE_ROOT,
    STAGING_SERVICE_ROOT)


def get_launchpad_object(config, filename=None, staging=False):
    '''Return an autheticated launchpad API object.'''
    if not filename:
        filename = config.CREDENTIALS

    if staging:
        SERVICE_ROOT = STAGING_SERVICE_ROOT
    else:
        SERVICE_ROOT = EDGE_SERVICE_ROOT

    if not os.path.exists(filename):
        launchpad = Launchpad.get_token_and_login('Tarmac',
            SERVICE_ROOT, config.CACHEDIR)
        launchpad.credentials.save(file(filename, 'w'))
    else:
        credentials = Credentials()
        credentials.load(open(filename))
        launchpad = Launchpad(credentials, SERVICE_ROOT,
            config.CACHEDIR)

    return launchpad


