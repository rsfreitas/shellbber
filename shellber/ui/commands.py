
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

# Application command environments
ENV_MAIN = 1
ENV_CONFIG = 2

# Common commands
CMD_CLEAR = 'clear'
CMD_HELP = 'help'
CMD_QUIT = 'quit'
CMD_QUIT_APP = 'app'

# Main commands
CMD_CHAT = 'chat'
CMD_CONTACT = 'contact'
CMD_CONTACT_ADD = 'add'
CMD_CONTACT_DEL = 'del'
CMD_CONTACT_LIST = 'list'
CMD_LOGIN = 'login'
CMD_LOGOUT = 'logout'
CMD_MSG = 'msg'
CMD_MSGTO = 'msgto'
CMD_REGISTER = 'register'
CMD_UNREGISTER = 'unregister'
CMD_MSGGR = 'msggr'
CMD_GROUP = 'group'
CMD_GROUP_CREATE = 'create'
CMD_GROUP_INVITE = 'invite'
CMD_GROUP_JOIN = 'join'
CMD_FILE = 'file'
CMD_FILETO = 'fileto'
CMD_UNCHAT = 'unchat'
CMD_CONFIG = 'config'
CMD_PRESENCE = 'presence'
CMD_PRESENCE_AWAY = 'away'
CMD_PRESENCE_ONLINE = 'online'
CMD_PRESENCE_OFFLINE = 'offline'
CMD_PRESENCE_AVAILABLE = 'available'
CMD_PRESENCE_INVISIBLE = 'invisible'

# Configuration commands
CMD_CFG_SET = 'set'
CMD_CFG_QUIT = 'quit'
CMD_CFG_SET_USERNAME = 'username'
CMD_CFG_SET_PASSWORD = 'password'
CMD_CFG_SET_SERVER = 'server'
CMD_CFG_SET_HOST = 'host'

class Commands(object):
    def __init__(self):
        self._commands = dict()
        self.add_command(CMD_CLEAR, 'Clear screen.')
        self.add_command(CMD_HELP,
                         'Gets a help description from an internal command or '
                         'this screen.', optional_arguments=1)

        self.add_command(CMD_QUIT,
                         'Quits application or an internal environment.',
                         optional_arguments=1,
                         sub_commands=[
                            self.sub_command(CMD_QUIT_APP,
                                             'Quits application directly.')
                         ])


    def __iter__(self):
        return iter(self._commands)


    def sub_command(self, command, help_, required=0, optional=0):
        cmd = dict()

        cmd[command] = {
            'help': help_,
            'required_arguments': required,
            'optional_arguments': optional,
        }

        return cmd


    def add_command(self, command, help_, sub_commands='', description='',
                    required_arguments=0, optional_arguments=0):
        cmd = self.sub_command(command, help_, required=required_arguments,
                               optional=optional_arguments)

        if sub_commands:
            cmd[command]['sub_commands'] = sub_commands

        if description:
            cmd[command]['description'] = description

        self._commands.update(cmd)


    def populate_commands(self):
        self._commands = collections.OrderedDict(sorted(self._commands.items()))


    def known_command(self, command):
        if self._commands.get(command) is None:
            return False

        return True


    def supported_commands(self):
        return self._commands.keys()


    def info(self, command):
        return self._commands.get(command)


    def _full_help(self):
        # TODO: Show actual enviroment
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

            if info.has_key('sub_commands'):
                cmd_help += '\nSupported sub-commands:\n\n'

                for sub_cmd in info['sub_commands']:
                    sub_info= sub_cmd.get(sub_cmd.keys()[0])
                    cmd_help += '  ${cmd}%-10s${ccmd}\t%s\n' % \
                            (sub_cmd.keys()[0], sub_info['help'])

            if info.has_key('description'):
                cmd_help += '\nDescription:\n\n'
                cmd_help += info['description']

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


    def validate(self, cmd):
        """
        Function to validate if @cmd is known and, if supports, has its
        arguments correct.

        :param cmd: The command to validate.

        :return Raises an exception if the command is invalid.
        """
        args = cmd.get(shellber.ui.input.ARGUMENTS, 'empty').split(' ')
        info = cmd.get(shellber.ui.input.INFO)

        if cmd.get(shellber.ui.input.COMMAND) not in self._commands:
            raise Exception("Unknown command")

        if info['required_arguments'] > 0:
            tests = [
                len(args) >= info['required_arguments'],
                args[0] != 'empty'
            ]

            if not all(tests):
                raise Exception("Wrong arguments, see help for details")

        if info.has_key('sub_commands') and args[0] != 'empty':
            if args[0] not in [s.keys()[0] for s in info['sub_commands']]:
                raise Exception("Unknown argument, see help for details")



class UserCommands(Commands):
    def __init__(self):
        super(UserCommands, self).__init__()
        self.add_command(CMD_LOGIN, 'Makes a login into a server.',
                         optional_arguments=4,
                         description='This command requires at least 3 '
                                     'arguments: username, password and '
                                     'server.\nIt also accepts a 4th '
                                     'where we pass the hostname of the '
                                     'service into the server.\n\nExample:\n\n'
                                     '  ${cmd}login${ccmd} user password '
                                     'jabber.com [service]\n')

        self.add_command(CMD_MSG, 'Sends a message to the active contact.',
                         required_arguments=1)

        self.add_command(CMD_MSGTO, 'Sends a message to a specific contact.',
                         required_arguments=2)

        self.add_command(CMD_MSGGR, 'Sends a message to a group.',
                         required_arguments=2)

        self.add_command(CMD_CHAT,
                         'Creates a virtual chat room with a specific contact.',
                         required_arguments=1,
                         description='This command must receive as argument '
                                     'a contact name to establish a chat with '
                                     'it.\n')

        self.add_command(CMD_UNREGISTER,
                         'Unregister an account, or try to, from a server.')

        self.add_command(CMD_GROUP, 'Manipulates chat groups.',
                         required_arguments=2,
                         sub_commands=[
                             self.sub_command(CMD_GROUP_CREATE,
                                              'Create groups'),
                             self.sub_command(CMD_GROUP_INVITE,
                                              'Invite users to group chat'),
                             self.sub_command(CMD_GROUP_JOIN,
                                              'Join a group chat')],
                         description='Only a brief description')

        self.add_command(CMD_CONTACT, 'Manipulates the user contacts.',
                         required_arguments=1,
                         sub_commands=[
                             self.sub_command(CMD_CONTACT_ADD,
                                              'Adds a contact into the user '
                                              'list.'),
                             self.sub_command(CMD_CONTACT_DEL,
                                              'Deletes a contact from the '
                                              'user list.'),
                             self.sub_command(CMD_CONTACT_LIST,
                                              'List all contacts from the '
                                              'user list.')
                         ])

        self.add_command(CMD_PRESENCE, 'Sets the user presence to others.',
                         required_arguments=1,
                         sub_commands=[
                             self.sub_command(CMD_PRESENCE_AWAY,
                                              'Sets presence as away.'),
                             self.sub_command(CMD_PRESENCE_ONLINE,
                                              'Sets presence as online.'),
                             self.sub_command(CMD_PRESENCE_AVAILABLE,
                                              'Sets presence as available to '
                                              'chat.'),
                             self.sub_command(CMD_PRESENCE_OFFLINE,
                                              'Sets presence as offline.'),
                             self.sub_command(CMD_PRESENCE_INVISIBLE,
                                              'Sets presence as invisible.')
                         ])

        self.add_command(CMD_FILE, 'Sends a file to the active contact.')
        self.add_command(CMD_FILETO, 'Sends a file to a specific contact.')
        self.add_command(CMD_REGISTER, 'Register an account.')
        self.add_command(CMD_LOGOUT, 'Makes the logout from a server.')
        self.add_command(CMD_UNCHAT, 'Closes an active chat room.')
        self.add_command(CMD_CONFIG, 'Enter in config mode.')
        self.populate_commands()



class ConfigCommands(Commands):
    def __init__(self):
        super(ConfigCommands, self).__init__()
        self.add_command(CMD_CFG_SET, 'Sets a config value.',
                         required_arguments=2,
                         sub_commands=[
                             self.sub_command(CMD_CFG_SET_USERNAME,
                                              'Configures the username.'),
                             self.sub_command(CMD_CFG_SET_PASSWORD,
                                              'Configures the password.'),
                             self.sub_command(CMD_CFG_SET_SERVER,
                                              'Configures the server name.'),
                             self.sub_command(CMD_CFG_SET_HOST,
                                              'Configures the server service '
                                              'host name.'),
                         ])

        self.populate_commands()



