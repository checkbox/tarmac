#!/usr/bin/env python

import os
import sys

from bzrlib import branch
from bzrlib.plugin import load_plugins
from launchpadlib.launchpad import Credentials, Launchpad

from tarmac.config import TarmacConfig

load_plugins()

configuration = TarmacConfig()

cachedir = '/tmp/tarmac-cache-%(pid)s' % {'pid': os.getpid()}
print 'Caching to %(cachedir)s' % {'cachedir': cachedir}

if not os.path.exists(configuration.CREDENTIALS):
    launchpad = Launchpad.get_token_and_login('Tarmac',
        'https://api.launchpad.dev/beta/', cachedir)
    launchpad.credentials.save(file(configuration.CREDENTIALS, 'w'))
else:
    credentials = Credentials()
    credentials.load(open(configuration.CREDENTIALS))
    launchpad = Launchpad(credentials, 'https://api.launchpad.dev/beta/',
        cachedir)

project = launchpad.projects['loggerhead']
try:
    trunk_entry = project.development_focus.branch
except AttributeError:
    print ('Oops!  It looks like you\'ve forgotten to specify a development '
    'focus branch.  Please link your "trunk" branch to the trunk '
    'development focus.')
    sys.exit()

candidates = []
for entry in trunk_entry.landing_candidates:
    print entry.source_branch.display_name
    if entry.queue_status == u'Approved':
        print '      will land.'
        candidates.append(entry)

#for candidate in candidates:
    #print 'Branching %s to %s' % (candidate.target_branch.bzr_identity,
    #    '/tmp/123456')
    #trunk = branch.Branch.open(candidate.target_branch.bzr_identity)
    #source = branch.Branch.open(candidate.source_branch.bzr_identity)
    #trunk_checkout = trunk.create_checkout('/tmp/1234561')

    #trunk_tree.merge(candidate.source_branch.bzr_identity)
    # TODO: Add hook code.
    #trunk_tree.commit(candidates.all_comments.entries[0])
    #trunk.push(trunk_remote)

