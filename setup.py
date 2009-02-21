#!/usr/bin/env python
'''Tarmac installation script.'''

from distutils.core import setup

from tarmac import __version__

setup(
    name=u'Tarmac',
    version=__version__,
    description=u'Tarmac - The Launchpad Lander',
    url=u'http://edge.launchpad.net/tarmac',
    license=u'AGPLv3',
    packages=['tarmac'],
    scripts=['lander.py'],
    long_description='''
        Tarmac is a series of scripts to facilitate the landing of Bazaar
        branches in Launchpad (http://edge.launchpad.net).''',
    )

