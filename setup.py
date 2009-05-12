#!/usr/bin/env python
# Copyright 2009 Paul Hummer - See LICENSE
'''Tarmac installation script.'''

from distutils.core import setup

from tarmac import __version__

setup(
    name=u'Tarmac',
    version=__version__,
    description=u'Tarmac - The Launchpad Lander',
    url=u'http://edge.launchpad.net/tarmac',
    license=u'AGPLv3',
    package_dir={
        'bzrlib.plugins.tarmac': 'bzrplugin',
        'tarmac': 'tarmac'},
    packages=['bzrlib.plugins.tarmac', 'tarmac'],
    scripts=['tarmac-lander'],
    long_description='''
        Tarmac is a series of scripts to facilitate the landing of Bazaar
        branches in Launchpad (http://edge.launchpad.net).''',
    )

