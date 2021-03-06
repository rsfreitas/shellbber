
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

from shellber.chat import chat

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
        self._env = commands.ENV_MAIN
        self._input = input.Input(self._output, self._env)
        self._present_credentials()

        # Start XMPP handling
        self._chat = chat.Chat(self.display_received_message)

        # Puts the application into the running mode ;-)
        self._args = args
        self._run = True


    def _present_credentials(self):
        self._output.message("Welcome to the ${FG_CYAN}shellber${FG_RESET} XMPP "
                             "client!")

        self._output.message("Enter a known command or ${cmd}help${ccmd} to "
                             "get a list of supported commands.")


    def _unsupported_command(self, *unused):
        self._output.error("Unsupported command")


    def _help(self, cmd):
        self._output.message(self._input.commands.help(cmd))


    def _login(self, cmd):
        args = cmd.get(input.ARGUMENTS)

        # No arguments, we'll use the configured account
        if args is None:
            # FIXME: We need to improve here... ;-), substitute dictionary
            #        keys with config constants
            try:
                if all(key in self._cfg.account for key in ('username',
                                                            'password',
                                                            'server',
                                                            'host')):
                    args = self._cfg.account['username'] + " " + \
                        self._cfg.account['password'] + " " + \
                        self._cfg.account['server'] + " " + \
                        self._cfg.account['host']
                else:
                    self._output.error("Missing account configuration details. "
                                       "You may do this through the config "
                                       "environment. 1")

                    return
            except:
                self._output.error("Missing account configuration details. "
                                   "You may do this through the config "
                                   "environment. 2")

                return

        try:
            self._chat.login(args.split())
            self._input.set_prompt(login=self._chat.ID)
        except Exception as error:
            self._output.error("Error: " + str(error))


    def _logout(self, cmd):
        try:
            self._chat.logout()
            self._input.set_prompt()
        except Exception as error:
            self._output.error("Error: " + str(error))


    def _start_chat(self, cmd):
        args = cmd.get(input.ARGUMENTS).split()
        contact = args[0]

        try:
            self._chat.start_chat(contact)
            self._input.set_prompt(login=self._chat.ID,
                                   contact=self._chat.contact)
        except Exception as error:
            self._output.error("Error: " + str(error))


    def _stop_chat(self, cmd):
        try:
            self._chat.stop_chat()
            self._input.set_prompt(login=self._chat.ID)
        except Exception as error:
            self._output.error("Error: " + str(error))


    def _register(self, cmd):
        self._chat.register()


    def _unregister(self, cmd):
        self._chat.unregister()


    def _group(self, cmd):
        # Are we calling which 'group' sub-command?
        args = cmd.get(input.ARGUMENTS).split()

        try:
            if args[0] == commands.CMD_GROUP_CREATE:
                self._chat.group_create(args[1])
            elif args[0] == commands.CMD_GROUP_INVITE:
                self._chat.group_invite(args[1:])
            elif args[0] == commands.GROUP_JOIN:
                self._chat.group_join(args[1])
            else:
                self._unsupported_command(args)
        except Exception as error:
            self._output.error("Error: " + str(error))


    def _quit(self, cmd):
        """
        Quits an application environment or the application itself.

        :param cmd: The command entered by the user.
        """
        args = cmd.get(input.ARGUMENTS, 'empty').split()
        tests = [
            self._env == commands.ENV_MAIN,
            args[0] == commands.CMD_QUIT_APP
        ]

        if any(tests):
            self._run = False
        elif self._env == commands.ENV_CONFIG:
            self._input.set_prompt(login=self._chat.ID,
                                   contact=self._chat.contact)

            self._env = commands.ENV_MAIN
            self._input.update_completer(self._env)


    def _config(self, cmd):
        """
        Enters in the application config environment.

        :param cmd: The command entered by the user.
        """
        self._input.set_prompt(login=self._chat.ID, contact=self._chat.contact,
                               environment='config')

        self._env = commands.ENV_CONFIG
        self._input.update_completer(self._env)


    def _contacts(self, cmd):
        args = cmd.get(input.ARGUMENTS).split()

        try:
            if args[0] == commands.CMD_CONTACT_ADD:
                self._chat.contact_add(args[1])
            elif args[0] == commands.CMD_CONTACT_DEL:
                self._chat.contact_del(args[1])
            elif args[0] == commands.CMD_CONTACT_LIST:
                self._chat.contact_list()
            else:
                self._unsupported_command(args)
        except Exception as error:
            self._output.error("Error: " + str(error))


    def _file(self, cmd):
        """
        Sends a file to the active contact in the chat.

        :param cmd: The command entered by the user.
        """
        pass


    def _fileto(self, cmd):
        """
        Sends a file directly to a specific user or a group. We must receive the
        first part of the command argument as the user/group name.

        :param cmd: The command entered by the user.
        """
        pass


    def _message(self, cmd):
        """
        Sends a message to the active contact in the chat.

        :param cmd: The command entered by the user.
        """
        args = cmd.get(input.ARGUMENTS)

        try:
            self._chat.message(args)
        except Exception as error:
            self._output.error("Error: " + str(error))


    def _msgto(self, cmd):
        """
        Sends a message directly to a specific user or a group. Here we must
        receive the first part of the command argument as the user/group name.

        :param cmd: The command entered by the user.
        """
        args = cmd.get(input.ARGUMENTS).split(' ', 1)

        try:
            self._chat.message(args[1], destination=args[0])
        except Exception as error:
            self._output.error("Error: " + str(error))


    def _cfg_set(self, cmd):
        args = cmd.get(input.ARGUMENTS).split()

        if hasattr(self._cfg, 'account') is False:
            self._cfg.account = dict()

        self._cfg.account[args[0]] = args[1]


    def _cfg_show(self, *unused):
        self._output.message(config.display_configurations(self._cfg))


    def display_received_message(self, message):
        pass


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


    def sync_configuration(self):
        """
        Writes our internal configuration to the application config file.
        """
        config.save(self._cfg)


    def handle_command(self, cmd):
        """
        A function to handle a previously entered command by the user. If the
        command read requires a function call, that function will be called
        receiving as argument the command dict info.

        :param cmd: The previously entered command.
        """
        if len(cmd.get(input.COMMAND)) < 1:
            return

        try:
            self._input.commands.validate(cmd)
        except Exception as error:
            self._output.error(str(error))
            return

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
            commands.CMD_CONFIG: self._config,
            commands.CMD_CONTACT: self._contacts,
            commands.CMD_FILE: self._file,
            commands.CMD_FILETO: self._fileto,
            commands.CMD_MSG: self._message,
            commands.CMD_MSGGR: self._msgto,
            commands.CMD_MSGTO: self._msgto,
            commands.CMD_CFG_SET: self._cfg_set,
            commands.CMD_CFG_SHOW: self._cfg_show,
            commands.CMD_CLEAR: output.clear,
            commands.CMD_QUIT: self._quit,
        }.get(cmd[input.COMMAND], self._unsupported_command)

        if callable(action):
            action(cmd)
        else:
            self._run = action



