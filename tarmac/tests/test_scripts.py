# Copyright (c) 2009 - Paul Hummer
'''Tests for Tarmac scripts.'''
import os
import sys
import unittest

from tarmac.bin import TarmacLander
from tarmac.exceptions import NoCommitMessage


class MockBMPComment:
    '''A mock merge proposal comment.'''
    title = 'This is a title.'
    message_body = 'This is a comment.'


def make_comment_list(count=5):
    '''Make a list of comments.'''
    comments = []
    for i in range(0,count):
        comments.append(MockBMPComment())
    return comments

class TestTarmacLander(unittest.TestCase):
    '''Tests for TarmacLander.'''

    def test_lander_dry_run(self):
        '''Test that setting --dry-run sets the dry_run property.'''
        sys.argv = ['foo', '--dry-run']
        script = TarmacLander()
        self.assertTrue(script.dry_run)

    def test_find_commit_message_from_title(self):
        '''Test getting a commit message from a title.'''
        script = TarmacLander()
        comments = make_comment_list()

        comments[4].title = u'Commit message'
        comments[4].message_body = u'All your base...'

        commit_message = script._find_commit_message(comments)
        self.assertEqual(commit_message, u'All your base...')

    def test_find_commit_mesage_from_message_body(self):
        '''Test getting a commit message from a message_body.'''
        script = TarmacLander()
        comments = make_comment_list()

        comments[4].message_body = u'Commit message: I\'m in ur code.'

        commit_message = script._find_commit_message(comments)
        self.assertEqual(commit_message, u'I\'m in ur code.')

    def test_find_commit_message_no_commit_message(self):
        '''Test that _find_commit_message raises NoCommentFound.'''
        script = TarmacLander()
        comments = make_comment_list()

        self.assertRaises(
            NoCommitMessage,
            script._find_commit_message, comments)


