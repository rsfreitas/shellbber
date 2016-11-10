
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



class Input(object):
    def __init__(self):
        self._prompt = '$> '
        self._options = {
            'register': 'Register a XMPP account.',
            'login': 'Makes a login into a XMPP server.',
            'logout': 'Makes the logout from a XMPP account.',
            'quit': 'Quits application.',
            'list': 'Lists our roster contacts.',
            'help': 'Gets a help description from an internal command.'
        }

        readline.set_completer(_Completer(self._options.keys()).complete)
        readline.parse_and_bind('tab: complete')


    def help(self):
        print "Available internal commands"
        print "===========================\n"
        print "%-20s\tDescription" % 'Command'
        print "-------             \t-----------\n"

        for command, description in self._options.iteritems():
            print '%-20s\t%s' % (command, description)


    def change_prompt(self):
        pass


    def change_color(self):
        pass


    def readline(self):
        line = raw_input(self._prompt)
        return line



