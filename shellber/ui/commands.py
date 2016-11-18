
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
Module to handle all supported terminal commands.
"""

import collections

import shellber.ui.input

# Supported commands
CMD_CHAT = 'chat'
CMD_CLEAR = 'clear'
CMD_HELP = 'help'
CMD_LIST = 'list'
CMD_LOGIN = 'login'
CMD_LOGOUT = 'logout'
CMD_MSG = 'msg'
CMD_MSGTO = 'msgto'
CMD_QUIT = 'quit'
CMD_REGISTER = 'register'
CMD_UNREGISTER = 'unregister'
CMD_MSGGR = 'msggr'
CMD_GROUP = 'group'
CMD_GROUP_CREATE = 'create'
CMD_GROUP_INVITE = 'invite'
CMD_GROUP_JOIN = 'join'

class UserCommands(object):
    def __init__(self):
        self._commands = dict()
        self._populate_commands()
        self._commands = collections.OrderedDict(sorted(self._commands.items()))


    def __iter__(self):
        return iter(self._commands)


    def _add_command(self, command, help_, description='', arguments='',
                     required_arguments=0, optional_arguments=0):
        self._commands[command] = {
            'help': help_,
            'description': description,
            'required_arguments': required_arguments,
            'optional_arguments': optional_arguments,
            'arguments': arguments
        }


    def _populate_commands(self):
        self._add_command(CMD_REGISTER, 'Register a XMPP account.')
        self._add_command(CMD_LOGIN, 'Makes a login into a XMPP server.')
        self._add_command(CMD_MSG, 'Sends a message to the active contact.')
        self._add_command(CMD_LIST, 'Show all contacts from the user roster.')
        self._add_command(CMD_QUIT, 'Quits application.')
        self._add_command(CMD_LOGOUT, 'Makes the logout from a XMPP server.')
        self._add_command(CMD_MSGTO, 'Sends a message to a specific contact.')
        self._add_command(CMD_CLEAR, 'Clear screen.')
        self._add_command(CMD_MSGGR, 'Sends a message to a group.')
        self._add_command(CMD_HELP,
                          'Gets a help description from an internal command or '
                          'this screen.', optional_arguments=1)

        self._add_command(CMD_CHAT,
                          'Creates a virtual chat room with a specific contact.')

        self._add_command(CMD_UNREGISTER,
                          'Unregister an account from a XMPP server.')

        self._add_command(CMD_GROUP, 'Manipulates chat groups.',
                          required_arguments=1,
                          arguments=[CMD_GROUP_CREATE, CMD_GROUP_INVITE,
                                     CMD_GROUP_JOIN])


    def known_command(self, command):
        if self._commands.get(command) is None:
            return False

        return True


    def supported_commands(self):
        return self._commands.keys()


    def info(self, command):
        return self._commands.get(command)


    def _full_help(self):
        cmd_help = "${FG_YELLOW}==============================\n"
        cmd_help += "= Shellber internal commands =\n"
        cmd_help += "==============================\n\n"
        cmd_help += "%-15s\tDescription\n" % 'Command'
        cmd_help += "-------        \t-----------${FG_RESET}\n"

        for command in self.supported_commands():
            info = self.info(command)
            cmd_help += '${cmd}%-15s${ccmd}\t%s\n' % (command, info['help'])

        return cmd_help


    def _cmd_help(self, arguments):
        # Arguments from a command usually will be separated by a space. So,
        # we get the first one to known which command will have its usage
        # returned.
        cmd_to_show = arguments.split(' ')[0]
        info = self.info(cmd_to_show)
        cmd_help = ''

        if info is None:
            cmd_help += '${FG_RED}Unknown command.${FG_RESET}\n'
        else:
            cmd_help += '${cmd}%s${ccmd} - %s\n' % \
                    (cmd_to_show, info.get('help'))

            cmd_help += '\nSupported arguments:\n\n'

            for sub_cmd in info['arguments']:
                cmd_help += '${cmd}%s${ccmd}\n' % sub_cmd

        return cmd_help


    def help(self, cmd):
        """
        Creates a text containing some help either from all the supported
        commands or a specific one.

        :param cmd: The command to known its description.
        """
        cmd_help = ''
        cmd_args = cmd.get(shellber.ui.input.ARGUMENTS)

        # Do we need to show the main help or a specific command?
        if cmd_args is None:
            cmd_help += self._full_help()
        else:
            cmd_help += self._cmd_help(cmd_args)

        return cmd_help



