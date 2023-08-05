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
import shlex
import subprocess
import sys


class _OSInfo(object):

    @property
    def is_osx(self):
        return sys.platform.lower() == 'darwin'

    @property
    def is_linux(self):
        return sys.platform.startswith('linux')

os_info = _OSInfo()


class RunCommandError(ValueError):
    pass


def run(command, capture_output=True, use_shell=False, print_command=False,
        should_return_returncode=False, should_raise_when_fail=False):
    """
    :type command: str
    :type capture_output: bool
    :type use_shell: bool
    :type print_command: bool
    :type should_return_returncode: bool
    :type should_raise_when_fail: bool
    :rtype: (str, str, int) | (str, str)
    """
    use_shell = '&&' in command or '||' in command or use_shell
    if print_command:
        print(command)
    popen = subprocess.Popen(command if use_shell else shlex.split(command),
                             stdout=subprocess.PIPE if capture_output else None,
                             stderr=subprocess.PIPE if capture_output else None,
                             shell=use_shell)
    stdout, stderr = popen.communicate()
    return_code = popen.returncode
    if return_code != 0 and should_raise_when_fail:
        raise RunCommandError('Command execution returns {}'.format(return_code))

    def _process_output(raw_output):
        try:
            _output = raw_output.decode('utf-8')
        except ValueError:
            return raw_output
        else:
            return _output[:-1]  # strip last '\n'

    stdout = _process_output(stdout)
    stderr = _process_output(stderr)

    if should_return_returncode:
        return stdout, stderr, return_code
    else:
        return stdout, stderr


def has_command(command):
    """
    test wheather a command exists in current $PATH or not.
    :type command: str
    :rtype: bool
    """
    stdout, _, return_code = run('which {}'.format(command), should_return_returncode=True)
    return len(stdout) != 0 and return_code == 0
