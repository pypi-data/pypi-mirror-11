"""
Shell integration

See https://groups.google.com/d/msg/iterm2-discuss/URKCBtS0228/rs5Ive4PCAAJ
for documentation on the sequences,
https://github.com/gnachman/iterm2-website/tree/master/source/misc for example
implementations, and https://iterm2.com/shell_integration.html for a list of
what this lets you do in iTerm2.

Usage
=====

Say you have a basic REPL like

input> run-command
command output

where "input> " is the prompt, "run-command" is the command typed by the user,
and "command output" is the output of run-command. The basic REPL (in Python
3), would be

while True:
    before_prompt()
    print("input> ", end='')
    after_prompt()
    command = input()
    before_output()
    return_val = run_command(command)
    after_output(return_val)

(here return_val should be in the range 0-255).

Note that it is recommended to use the functions (like before_prompt()) rather
than the variables (like BEFORE_PROMPT) directly, as variables may break
readline's character counting.

"""
from __future__ import print_function, division, absolute_import

import sys

# The "FinalTerm" shell sequences

BEFORE_PROMPT = '\033]133;A\a'
AFTER_PROMPT = '\033]133;B\a'
BEFORE_OUTPUT = '\033]133;C\a'
AFTER_OUTPUT = '\033]133;D;{command_status}\a' # command_status is the command status, 0-255

# iTerm2 specific sequences. All optional.

SET_USER_VAR = '\033]1337;SetUserVar={user_var_key}={user_var_value}\a'
# The current shell integration version is 1. We don't use this as an outdated
# shell integration version would only prompt the user to upgrade the
# integration that comes with iTerm2.
SHELL_INTEGRATION_VERSION = '\033]1337;ShellIntegrationVersion={shell_integration_version}\a'

# REMOTE_HOST and CURRENT_DIR are best echoed right after AFTER_OUTPUT.

# remote_host_hostname should be the fully qualified hostname. Integrations
# should allow users to set remote_host_hostname in case DNS is slow.
REMOTE_HOST = '\033]1337;RemoteHost={remote_host_username}@{remote_host_hostname}\a'
CURRENT_DIR = '\033]1337;CurrentDir={current_dir}\a'

def before_prompt():
    """
    Shell sequence to be run before the prompt.
    """
    sys.stdout.write(BEFORE_PROMPT)

def after_prompt():
    """
    Shell sequence to be run after the prompt.
    """
    sys.stdout.write(AFTER_PROMPT)

def before_output():
    """
    Shell sequence to be run before the command output.
    """
    sys.stdout.write(BEFORE_OUTPUT)

def after_output(command_status):
    """
    Shell sequence to be run after the command output.

    The command_status should be in the range 0-255.
    """
    if command_status not in range(256):
        raise ValueError("command_status must be an integer in the range 0-255")
    sys.stdout.write(AFTER_OUTPUT.format(command_status=command_status))
