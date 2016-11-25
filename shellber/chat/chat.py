
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
A module to handle chat between users.
"""

import logging

class Chat(object):
    def __init__(self):
        self._connected = False
        self._password = ''
        self.username = ''
        self.server = ''
        self.host = ''
        self.ID = ''
        self.contact = ''


    def register(self):
        pass


    def unregister(self):
        pass


    def login(self, args):
        if self._connected:
            raise Exception("already connected")

        self.username = args[0]
        self._password = args[1]
        self.server = args[2]

        # Build the user ID
        self.ID = self.username + "@" + self.server

        if len(args) > 3:
            self.host = args[3]
            self.ID += "/" + self.host

        self._connected = True


    def logout(self):
        if self._connected is False:
            raise Exception("not connected")

        self._connected = False
        self.contact = ''
        self.ID = ''


    def message(self, message, destination=''):
        if self._connected is False:
            raise Exception("not connected")

        pass


    def start_chat(self, contact):
        if self._connected is False:
            raise Exception("not connected")

        self.contact = contact


    def stop_chat(self):
        if self._connected is False:
            raise Exception("not connected")

        self.contact = ''


    def group_create(self, group_name):
        if self._connected is False:
            raise Exception("not connected")

        pass


    def group_invite(self, users):
        if self._connected is False:
            raise Exception("not connected")

        pass


    def group_join(self, group_name):
        if self._connected is False:
            raise Exception("not connected")

        pass


    def contact_add(self, name):
        pass


    def contact_del(self, name):
        pass


    def contact_list(self):
        pass



