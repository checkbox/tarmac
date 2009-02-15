#!/usr/bin/env python

from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.get_token_and_login('Tarmac',
    STAGING_SERVICE_ROOT, cachedir)
#launchpad.credentials.save(file(LOGIN_CREDENTIALS, 'w'))

project = launchpad.projects['entertainer']
trunk = entertainer.development_focus.branch


candidates = [entry for entry in trunk['landing_candidates'].entries
                    if entry.queue_status == 'Approved']

for candidate in candidates:
    # Branch trunk & build
    # Merge
    # Run Hooks
    # Commit
    # Push

