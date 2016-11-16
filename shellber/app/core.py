
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

import shellber.app.config as config

from shellber.ui import input
from shellber.ui import ui

class Application(object):
    """
    A class to hold all important informations from the application. Its
    objective is control the application execution. One may used like this:

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
        # - signal monitoring
        # - logging

        # Start user-input handling
        self._args = args
        self._input = input.Input()
        self._present_credentials()

        self._run = True


    def _present_credentials(self):
        self._input.message("Welcome the ${FG_CYAN}shellber${FG_RESET} XMPP "
                            "client!")

        self._input.message("Enter a known command or ${cmd}help${ccmd} to "
                            "get a list of supported commands.")


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
        A function to handle a previously entered command by the user.

        :param cmd: The previously entered command.
        """
        # A list of actions to take on every supported command
        action = {
            'help': self._input.help,
            'clear': ui.clear,
            'quit': False
        }.get(cmd['command'], True)

        if callable(action):
            action(cmd)
        else:
            self._run = action



