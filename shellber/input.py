
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
Functions to handle user input.
"""

import collections
import readline

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



class _UserCommand(collections.Iterator):
    def __init__(self):
        self._commands = dict()
        self._populate_commands()


    def _add_command(self, command, help_, description='', arguments=0):
        self._commands[command] = {
            'help': help_,
            'description': description,
            'number_of_arguments': arguments
        }


    def _populate_commands(self):
        self._add_command('register', 'Register a XMPP account.')
        self._add_command('login', 'Makes a login into a XMPP server.')
        self._add_command('msg', 'Sends a message to the active contact.')
        self._add_command('help', 'Gets a help description from an internal \
command or this screen.')

        self._add_command('list', 'Show all contacts from the user roster.')
        self._add_command('quit', 'Quits application.')
        self._add_command('logout', 'Makes the logout from a XMPP server.')
        self._add_command('msgto', 'Sends a message to a specific contact.')
        self._add_command('chat', 'Creates a virtual chat room with a specific \
contact.')

        self._commands = collections.OrderedDict(sorted(self._commands.items()))


    def next(self):
        pass


    def supported_commands(self):
        return self._commands.items()


    def command_info(self, command):
        return self._commands.get(command, None)



class Input(object):
    """
    A class to handle the input from the user.
    """
    def __init__(self):
        self._prompt = '$> '
        self._options = {
            'register': {
                'help': 'Register a XMPP account.',
                'description': '',
                'number_of_arguments': ''
            },
            'login': {
                'help': 'Makes a login into a XMPP server.',
                'description': ''
            },
            'logout': {
                'help': 'Makes the logout from a XMPP account.',
                'description': ''
            },
            'quit': {
                'help': 'Quits application.',
                'description': ''
            },
            'list': {
                'help': 'Lists our roster contacts.',
                'description': ''
            },
            'help': {
                'help': 'Gets a help description from an internal command.',
                'description': ''
            },
            'msg': {
                'help': 'Sends a message to the active contact.',
                'description': ''
            },
            'msgto': {
                'help': 'Sends a message to a specific contact.',
                'description': ''
            },
            'chat': {
                'help': 'Creates a virtual chat room with a specific contact.',
                'description': ''
            }
        }

        self._options = collections.OrderedDict(sorted(self._options.items()))
        readline.set_completer(_Completer(self._options.keys()).complete)
        readline.parse_and_bind('tab: complete')


    def help(self, cmd):
        # Did we need to show the main help?
        if len(cmd) == 1:
            print "=========================="
            print "Shellber internal commands"
            print "==========================\n"
            print "%-20s\tDescription" % 'Command'
            print "-------             \t-----------\n"

            for command, info in self._options.iteritems():
                print '%-20s\t%s' % (command, info['help'])

            print ''
        else:
            # Or a specific command?
            cmd_to_show = cmd.get('arguments')
            cmd_info = self._options.get(cmd_to_show.split(' ')[0])

            if cmd_info is None:
                print 'Unknown command.'
            else:
                print '%s - %s' % (cmd_to_show, cmd_info.get('help'))

        return True


    def change_prompt(self):
        pass


    def readline(self):
        """
        Reads the input from the user. We expect to receive a known command
        and its required arguments.

        :return Returns a dictionary with the command and its arguments such
                as: {'command': 'help', 'arguments': 'list'}
        """
        line = raw_input(self._prompt)

        # We always have a command beggining the line. At least that's
        # the expected.
        data = line.split(' ', 1)

        command = dict()
        command['command'] = data[0]

        if len(data) > 1:
            command['arguments'] = data[1]

        return command


    def message(self, message):
        """
        Shows a message into the standard output with the default prompt.

        :param message: The message to be show.
        """
        # TODO: change the message, putting some colors into the keywords
        print '%s%s' % (self._prompt, message)



