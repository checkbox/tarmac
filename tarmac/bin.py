# Copyright (c) 2009 - Paul Hummer
'''Code used by Tarmac scripts.'''
import os
import sys

from bzrlib import branch, bzrdir
from bzrlib.plugin import load_plugins
from launchpadlib.errors import HTTPError
from launchpadlib.launchpad import Credentials, Launchpad, STAGING_SERVICE_ROOT

from tarmac.config import TarmacConfig

load_plugins()
DEV_SERVICE_ROOT = 'https://api.launchpad.dev/beta/'


def main():
    '''Tarmac script.'''
    configuration = TarmacConfig()

    cachedir = '/tmp/tarmac-cache-%(pid)s' % {'pid': os.getpid()}
    print 'Caching to %(cachedir)s' % {'cachedir': cachedir}

    if not os.path.exists(configuration.CREDENTIALS):
        launchpad = Launchpad.get_token_and_login('Tarmac',
            STAGING_SERVICE_ROOT, cachedir)
        launchpad.credentials.save(file(configuration.CREDENTIALS, 'w'))
    else:
        try:
            credentials = Credentials()
            credentials.load(open(configuration.CREDENTIALS))
            launchpad = Launchpad(credentials, STAGING_SERVICE_ROOT, cachedir)
        except HTTPError:
            print ('Oops!  It appears that the OAuth token is invalid.  Please '
            'delete %(credential_file)s and re-authenticate.' %
                {'credential_file': configuration.CREDENTIALS})
            sys.exit()

    project = launchpad.projects['loggerhead']
    try:
        trunk = project.development_focus.branch
    except AttributeError:
        print ('Oops!  It looks like you\'ve forgotten to specify a development '
        'focus branch.  Please link your "trunk" branch to the trunk '
        'development focus.')
        sys.exit()

    candidates = [entry for entry in trunk.landing_candidates
                    if entry.queue_status == u'Approved']

    for candidate in candidates:
        temp_dir = '/tmp/merge-%(source)s-%(pid)s' % {
            'source': candidate.source_branch.name,
            'pid': os.getpid()
            }
        os.mkdir(temp_dir)

        accelerator, target_branch = bzrdir.BzrDir.open_tree_or_branch(
            candidate.target_branch.bzr_identity)
        target_tree = target_branch.create_checkout(
            temp_dir, None, True, accelerator)
        source_branch = branch.Branch.open(candidate.source_branch.bzr_identity)

        target_tree.merge_from_branch(source_branch)
        # TODO: Add hook code.
        trunk_tree.commit(candidate.all_comments[0].message_body)



