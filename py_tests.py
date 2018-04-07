#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, sys, subprocess
class PreCommitCheck(object):
    """
    Checks if tests were written/modified, before proceeding with `git commit`.
    """
    EXIT_OK = 0
    EXIT_ERROR = 1
    @staticmethod
    def _construct_test_filepath(filepath):
        TAGS = 'tags'
        parts = filepath.split('/')
        test_parts = parts[0:-1] + ['tests']
        if TAGS in parts[-1]:
            test_file = 'test_{0}.py'.format(TAGS)
        else:
            test_file = 'test_{0}'.format(parts[-1])
        test_parts.append(test_file)
        return '/'.join(test_parts)
    @staticmethod
    def _get_staged_files():
        git_status = subprocess.check_output(["git", "status", "--porcelain"])
        regex = r'[M|A]  (?P<name>[\w+\.\/-]+).py'
        files = re.findall(regex, git_status)
        return ['{0}.py'.format(f) for f in files]
    @classmethod
    def check_if_tests_modified(cls):
        staged_files = cls._get_staged_files()
        for sf in staged_files:
            if 'test_' not in sf:
                test_filepath = cls._construct_test_filepath(sf)
                if test_filepath not in staged_files:
                    print "Test for {0} file is not written/modified!".format(sf)
                    sys.exit(cls.EXIT_ERROR)
        print "All created/modified files are tested! :D"
        sys.exit(cls.EXIT_OK)
if __name__ == "__main__":
    PreCommitCheck.check_if_tests_modified()
