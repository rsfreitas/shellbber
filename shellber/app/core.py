
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

        # Puts the application into the running mode ;-)
        self._args = args
        self._run = True


    def _present_credentials(self):
        self._output.message("Welcome to the ${FG_CYAN}shellber${FG_RESET} XMPP "
                             "client!")

        self._output.message("Enter a known command or ${cmd}help${ccmd} to "
                             "get a list of supported commands.")


    def _unsupported_command(self, *unused):
        self._output.message("${FG_RED}Unsupported command${FG_RESET}")


    def _help(self, cmd):
        self._output.message(self._input.commands.help(cmd))


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
            commands.CMD_CLEAR: output.clear,
            commands.CMD_QUIT: False
        }.get(cmd[input.COMMAND], self._unsupported_command)

        if callable(action):
            action(cmd)
        else:
            self._run = action



