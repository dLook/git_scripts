#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import os, re, sys, subprocess


class VarBust(object):
    VAR_BUST_SETUP = {
        'css': ['edit_me'],
        'js': ['edit_me']
    }

    @classmethod
    def update(cls):
        changed = cls._get_changed_file_extensions()
        if changed:
            new_var_bust = cls._get_new_var_bust()
            current_dir = os.getcwd()
            for item in changed:
                templates = cls.VAR_BUST_SETUP.get(item)
                for tmpl in templates:
                    file_path = '/'.join([current_dir, tmpl])
                    with open(file_path, 'r+') as f:
                        content = f.read()
                        current_var_bust = cls._get_current_var_bust(content, file_path)
                        new_content = content.replace(current_var_bust, new_var_bust)
                        f.truncate(0)
                        f.seek(0)
                        f.write(new_content)
                    cls._add_to_commit(tmpl)

    @classmethod
    def _get_changed_file_extensions(cls):
        git_status = subprocess.check_output(["git", "status", "--porcelain"])
        staged_files = git_status.split('\n')
        return set([sf.split('.')[-1] for sf in staged_files if sf.split('.')[-1] in cls.VAR_BUST_SETUP])

    @staticmethod
    def _get_current_var_bust(content, templ):
        regex = r"{% set_var '.*' as bust %}"
        match = re.findall(regex, content)
        if len(match) > 1:
            print "More than one var_bust param in template: {0}".format(templ)
            sys.exit(1)
        return match[0]

    @staticmethod
    def _get_new_var_bust():
        return "{{% set_var '{0}' as bust %}}".format(
            datetime.now().strftime('%Y%m%d%H%M'))

    @staticmethod
    def _add_to_commit(tmpl):
        subprocess.call(["git", "add", "{0}".format(tmpl)])
        print "File {0} added to commit!".format(tmpl)


if __name__ == "__main__":
    VarBust.update()
