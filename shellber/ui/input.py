
#
# Copyright (C) 2016 Rodrigo Freitas
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
Objects to handle user input.
"""

import readline

import shellber.ui.commands as commands

PROMPT = '$> '

# User command
COMMAND = 'command'
ARGUMENTS = 'arguments'
INFO = 'info'

class _Completer(object):
    def __init__(self, options):
        self.options = sorted(options)


    def complete(self, text, state):
        response = None

        if state == 0:
            if text:
                self.matches = [
                    s for s in self.options if s and s.startswith(text)
                ]
            else:
                self.matches = self.options[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None

        return response



class Input(object):
    """
    A class to handle the input from the user.
    """
    def __init__(self, output_, env):
        self._prompt = ''
        self._output = output_
        self._main_commands = commands.UserCommands()
        self._cfg_commands = commands.ConfigCommands()

        self.set_prompt()
        self.update_completer(env)
        readline.parse_and_bind('tab: complete')


    def update_completer(self, env):
        self.commands = {
            commands.ENV_MAIN: self._main_commands,
            commands.ENV_CONFIG: self._cfg_commands
        }.get(env)

        readline.set_completer(
            _Completer(self.commands.supported_commands()).complete)


    def set_prompt(self, login='', contact='', environment=''):
        self._prompt = ''

        if environment:
            self._prompt += '[${FG_GREEN}%s${FG_RESET}] ' % environment

        if login:
            self._prompt += '[${FG_CYAN}%s${FG_RESET}] ' % login

        if contact:
            self._prompt += '<--> [${FG_MAGENTA}%s${FG_RESET}] ' % contact

        self._prompt += PROMPT


    def readline(self):
        """
        Reads the input from the user. We expect to receive a known command
        and its required arguments.

        :return Returns a dictionary with the command and its arguments such
                as: {'command': 'help', 'arguments': 'list', 'info': dict}
        """
        try:
            line = raw_input(self._output.parse(self._prompt))
        except:
            return None

        # We always have a command beggining the line. At least that's
        # the expected.
        data = line.strip().split(' ', 1)

        command = dict()
        command[COMMAND] = data[0]

        if len(data) > 1:
            command[ARGUMENTS] = data[1]

        # Do we have a known command? Yes, insert its info too ;-)
        if self.commands.known_command(command[COMMAND]):
            command[INFO] = self.commands.info(command[COMMAND])

        return command



