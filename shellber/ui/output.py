
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
Functions do handle user interface output.
"""

import os
from string import Template

import colorama

def clear(*unused):
    """
    A function to clear the application console.
    """
    os.system('clear')



class Output(object):
    """
    A class to handle a little internal template language to make messages
    more user friendly.
    """
    def __init__(self):
        # Tokens to translate
        self._tokens = {
            'cmd': '${FG_GREEN}',
            'ccmd': '${FG_RESET}'
        }

        # Supported colors
        self._colors = {
            'FG_BLACK': colorama.Fore.BLACK,
            'FG_RED': colorama.Fore.RED,
            'FG_GREEN': colorama.Fore.GREEN,
            'FG_YELLOW': colorama.Fore.YELLOW,
            'FG_BLUE': colorama.Fore.BLUE,
            'FG_MAGENTA': colorama.Fore.MAGENTA,
            'FG_CYAN': colorama.Fore.CYAN,
            'FG_WHITE': colorama.Fore.WHITE,
            'FG_RESET': colorama.Fore.RESET,
            'BG_BLACK': colorama.Back.BLACK,
            'BG_RED': colorama.Back.RED,
            'BG_GREEN': colorama.Back.GREEN,
            'BG_YELLOW': colorama.Back.YELLOW,
            'BG_BLUE': colorama.Back.BLUE,
            'BG_MAGENTA': colorama.Back.MAGENTA,
            'BG_CYAN': colorama.Back.CYAN,
            'BG_WHITE': colorama.Back.WHITE,
            'BG_RESET': colorama.Back.RESET
        }


    def _preprocess(self, message):
        return Template(message).safe_substitute(self._tokens)


    def parse(self, message):
        """
        A function to parse a message with known tokens returning a message
        ready to be displayed to the user.

        :param message: The original message with/without tokens.

        :return Returns a new message.
        """
        return Template(self._preprocess(message)).safe_substitute(self._colors)


    def message(self, message):
        """
        A function to print messages to the application output.

        :param message: The message which will be printed into the standard
                        output.
        """
        print self.parse(message)



    def error(self, message):
        """
        A function to print error messages to the application output.

        :param message: The message which will be printed into the standard
                        output.
        """
        print self.parse("${FG_RED}%s${FG_RESET}" % message)



