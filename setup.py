#!/usr/bin/env python
# Copyright 2009 Paul Hummer
#
# This file is part of Tarmac.
#
# Tarmac is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by
# the Free Software Foundation.
#
# Tarmac is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tarmac.  If not, see <http://www.gnu.org/licenses/>.
'''Tarmac installation script.'''

from setuptools import setup

from tarmac import __version__


setup(
    author='Tarmac Developers',
    name=u'tarmac',
    version=__version__,
    description=u'Tarmac - The Launchpad Lander',
    url=u'https://launchpad.net/tarmac',
    license=u'GPLv3',
    package_dir={'tarmac': 'tarmac'},
    packages=['tarmac', 'tarmac.bin', 'tarmac.plugins', 'tarmac.tests'],
    test_suite='tarmac',
    scripts=['bin/tarmac'],
    data_files=[
        ('share/man/man1', ['docs/tarmac.1']),
        ('/etc/apparmor.d', ['data/tarmac.apparmor']),
    ],
    long_description='''
        Tarmac is a series of scripts to facilitate the landing of Bazaar
        branches in Launchpad (https://launchpad.net).''',
)
