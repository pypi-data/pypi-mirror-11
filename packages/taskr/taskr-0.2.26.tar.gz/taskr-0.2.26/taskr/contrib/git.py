#
# Copyright 2014-2015 sodastsai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import unicode_literals, division, absolute_import, print_function
from collections import OrderedDict
import os
from .system import run


# Ref: http://stackoverflow.com/questions/2657935/checking-for-a-dirty-index-or-untracked-files-with-git
# Ref: https://www.kernel.org/pub/software/scm/git/docs/git-status.html

class GitRepo(object):

    def __init__(self, source_root=None):
        self._source_root = source_root or os.getcwd()
        """:type: str"""

    @property
    def source_root(self):
        return self._source_root

    def run_git_command(self, command, capture_output=True, use_shell=False):
        """
        :type command: str
        :type capture_output: bool
        :type use_shell: bool
        :rtype: str
        """
        stdout, stderr = run('cd {} && git {}'.format(self.source_root, command),
                             capture_output=capture_output, use_shell=use_shell)
        if stderr:
            raise ValueError('Failed to run git command at "{}". stderr={}'.format(self.source_root, stderr))
        return stdout

    @property
    def config(self):
        result = {}
        for config_line in self.run_git_command('config --list').splitlines():
            config_line_components = config_line.split('=')
            raw_key = config_line_components[0]
            value = '='.join(config_line_components[1:])

            raw_key_components = raw_key.split('.')
            container = result
            for idx, raw_key_component in enumerate(raw_key_components):
                if raw_key_component not in container:
                    container[raw_key_component] = {}
                if idx != len(raw_key_components)-1:
                    container = container[raw_key_component]
                else:
                    container[raw_key_component] = value
        return result

    @property
    def head_hash(self):
        return self.run_git_command('rev-parse HEAD')

    @property
    def is_clean(self):
        """
        :rtype: bool
        """
        return len(self.status) == 0

    @property
    def status(self):
        """
        :rtype: OrderedDict[str, str]
        """
        result = OrderedDict()
        for stdout_line in self.run_git_command('status --porcelain').split('\n'):
            if stdout_line:
                result[stdout_line[2:].strip()] = stdout_line[:2]
        return result

    @property
    def tags(self):
        return self.run_git_command('tag').split('\n')

    @property
    def branches(self):
        return list(map(lambda x: x.strip().replace('* ', ''), self.run_git_command('branch').split('\n')))

    @property
    def current_branch(self):
        """
        :rtype: str
        """
        return self.run_git_command('branch | grep "*" | awk \'{print $2}\'')

    def changed_files(self, commit='HEAD', another_commit='HEAD^'):
        """
        :type commit: str
        :type another_commit: str
        :rtype: list[str]
        """
        result = self.run_git_command('diff-tree --no-commit-id --name-only -r {} {}'.format(commit, another_commit))
        return result.split('\n') if result else []

    def file_content(self, path, commit=''):
        """
        :type path: str
        :type commit: str
        :rtype: str | bytes
        """
        return self.run_git_command('show {}:{}'.format(commit, path))

    def add(self, *file_paths):
        """
        :type file_paths: list[str]
        """
        self.run_git_command('add {}'.format(' '.join(file_paths)))

    def commit(self, message):
        self.run_git_command('commit -m "{}"'.format(message))

    def reset(self, commit, hard=False):
        self.run_git_command('reset {} {}'.format('--hard' if hard else '--soft', commit))
