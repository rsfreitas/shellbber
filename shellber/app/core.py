
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
The shellber core module to control the application.
"""

import signal

import shellber.app.config as config
import shellber.app.log as log

from shellber.ui import input
from shellber.ui import output
from shellber.ui import commands

from shellber.xmpp import chat

class Application(object):
    """
    A class to hold all important informations from the application. Its
    objective is to control the application execution. One may used like this:

    app = Application()

    while app.run():
        cmd = app.wait_for_command()
        app.handle_command(cmd)

    :param args: An object from the command line options parser.
    """
    def __init__(self, args):
        # Start configuration
        self._cfg = config.load(args.config)

        if self._cfg is None:
            raise Exception("Invalid configuration!")

        # Start internals
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        log.start_log(self._cfg.log_filename, self._cfg.log_level)

        # Initialize application output environment
        self._output = output.Output()

        # Start user-input handling
        self._input = input.Input(self._output)
        self._present_credentials()

        # Start XMPP handling
        self._chat = chat.Chat()

        # Puts the application into the running mode ;-)
        self._args = args
        self._run = True
        self._ID = ''


    def _present_credentials(self):
        self._output.message("Welcome to the ${FG_CYAN}shellber${FG_RESET} XMPP "
                             "client!")

        self._output.message("Enter a known command or ${cmd}help${ccmd} to "
                             "get a list of supported commands.")


    def _unsupported_command(self, *unused):
        self._output.error("Unsupported command")


#    def _validate_command(self, cmd):
#        try:
#            self._input.commands.validate(cmd)
#        except Exception as error:
#            self._output.error(error)
#            return False
#
#        return True


    def _help(self, cmd):
        self._output.message(self._input.commands.help(cmd))


    def _login(self, cmd):
        if self._input.commands.validate(cmd) is False:
            self._output.message("${FG_RED}Invalid command.${FG_RESET} "
                                 "See ${cmd}help${ccmd} for details.")

            return

        args = cmd.get(input.ARGUMENTS).split(' ')

        if self._chat.login(args) is False:
            self._output.error("Error while login into the XMPP server.")
        else:
            self._ID = '[${FG_CYAN}%s@%s${FG_RESET}]' % \
                    (self._chat.username, self._chat.server)

            self._input.change_prompt(self._output.parse('%s ' % self._ID))


    def _logout(self, cmd):
        self._chat.logout()
        self._ID = ''
        self._input.change_prompt('')


    def _start_chat(self, cmd):
        if self._input.commands.validate(cmd) is False:
            self._output.message("${FG_RED}Invalid command.${FG_RESET} "
                                 "See ${cmd}help${ccmd} for details.")

            return

        args = cmd.get(input.ARGUMENTS).split(' ')
        contact = args[0]
        self._chat.start_chat(contact)
        self._input.change_prompt(self._output.parse(
                                  '%s <--> [${FG_MAGENTA}%s${FG_RESET}] ' % \
                                    (self._ID, contact)))


    def _stop_chat(self, cmd):
        self._chat.stop_chat()
        self._input.change_prompt(self._output.parse('%s ' % self._ID))


    def _register(self, cmd):
        self._chat.register()


    def _unregister(self, cmd):
        self._chat.unregister()


    def _message(self, cmd):
        self._chat.message()


    def _group(self, cmd):
        if self._input.commands.validate(cmd) is False:
            self._output.message("${FG_RED}Invalid command.${FG_RESET} "
                                 "See ${cmd}help${ccmd} for details.")

            return

        # Are we calling which 'group' sub-command?
        args = cmd.get(input.ARGUMENTS).split(' ')

        foo = {
            commands.CMD_GROUP_CREATE: self._chat.group_create,
            commands.CMD_GROUP_INVITE: self._chat.group_invite,
            commands.CMD_GROUP_JOIN: self._chat.group_join
        }.get(args[0], self._unsupported_command)

        foo(args)


    def run(self):
        """
        Checks if the application may still run.

        :return Returns True if the application may continue its execution or
                False otherwise.
        """
        return self._run


    def wait_for_command(self):
        """
        Waits for the user input command and return it.

        :return Returns the command entered by the user.
        """
        return self._input.readline()


    def handle_command(self, cmd):
        """
        A function to handle a previously entered command by the user. If the
        command read requires a function call, that function will be called
        receiving as argument the command dict info.

        :param cmd: The previously entered command.
        """
        # A list of actions to take on every supported command
        action = {
            commands.CMD_HELP: self._help,
            commands.CMD_LOGIN: self._login,
            commands.CMD_LOGOUT: self._logout,
            commands.CMD_REGISTER: self._register,
            commands.CMD_UNREGISTER: self._unregister,
            commands.CMD_GROUP: self._group,
            commands.CMD_CHAT: self._start_chat,
            commands.CMD_UNCHAT: self._stop_chat,
            commands.CMD_CLEAR: output.clear,
            commands.CMD_QUIT: False,
            '': True
        }.get(cmd[input.COMMAND], self._unsupported_command)

        if callable(action):
            action(cmd)
        else:
            self._run = action



