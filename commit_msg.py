#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


class CommitMsgCheck(object):
    EXIT_OK = 0
    EXIT_ERROR = 1
    ACCEPTABLE_LENGTH = 8
    ERROR_COLOR = "\033[1;31m"

    def __init__(self, temp_file):
        self.temp_file = temp_file

    @staticmethod
    def _get_commit_message(temp_file):
        with open(temp_file, 'r') as tf:
            commit_message = tf.read()
        return commit_message

    def validate(self):
        commit_message = self._get_commit_message(self.temp_file)
        if len(commit_message) <= self.ACCEPTABLE_LENGTH:
            sys.stdout.write(self.ERROR_COLOR + "Commit message is too short!\n")
            sys.exit(self.EXIT_ERROR)
        sys.exit(self.EXIT_OK)


if __name__ == "__main__":
    temp_file = sys.argv[1]
    commit_message = CommitMsgCheck(temp_file)
    commit_message.validate()

