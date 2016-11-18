
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
A module to handle application chat between users.
"""

class Chat(object):
    def __init__(self):
        self._active_contat = None
        self._connected = False
        self.username = ''
        self.server = ''
        self.host = ''
        self._password = ''


    def register(self):
        pass


    def unregister(self):
        pass


    def login(self, args):
        if len(args) < 3:
            return False

        self.username = args[0]
        self._password = args[1]
        self.server = args[2]

        if len(args) > 3:
            self.host = args[3]

        self._connected = True

        return True


    def logout(self):
        if self._connected is False:
            return

        self._connected = False
        self._active_contact = None


    def message(self):
        pass


    def start_chat(self, contact):
        self._active_contact = contact


    def group_create(self, cmd):
        pass


    def group_invite(self, cmd):
        pass


    def group_join(self, cmd):
        pass



