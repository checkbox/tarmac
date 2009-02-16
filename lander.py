#!/usr/bin/env python

from bzrlib import branch
from bzrlib.plugin import load_plugins
from launchpadlib.launchpad import Launchpad

load_plugins()

cachedir = '/tmp'

launchpad = Launchpad.get_token_and_login('Tarmac',
    'https://api.launchpad.dev/beta/', cachedir)
#launchpad.credentials.save(file(LOGIN_CREDENTIALS, 'w'))

project = launchpad.projects['gnome-terminal']
trunk_entry = project.development_focus.branch

candidates = []
for entry in trunk_entry.landing_candidates:
    if entry.queue_status == u'Approved':
        candidates.append(entry)

for candidate in candidates:
    print 'Branching %s to %s' % (candidate.target_branch.bzr_identity,
        '/tmp/123456')
    trunk = branch.Branch.open(candidate.target_branch.bzr_identity)
    source = branch.Branch.open(candidate.source_branch.bzr_identity)
    trunk_checkout = trunk.create_checkout('/tmp/1234561')

    #trunk_tree.merge(candidate.source_branch.bzr_identity)
    # TODO: Add hook code.
    #trunk_tree.commit(candidates.all_comments.entries[0])
    #trunk.push(trunk_remote)

