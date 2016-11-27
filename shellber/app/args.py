
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
Functions do handle command line arguments.
"""

import argparse

DEFAULT_CONFIG_FILE = 'shellber.yml'

def parse_command_line_arguments(progname, progversion, description):
    """
    Parse arguments from the command line.

    :param progname: The application name.
    :param progversion: The application version.
    :param description: A brief description of the application usage.

    :return
    """
    usage = '%(prog)s [OPTIONS]'

    parser = argparse.ArgumentParser(prog=progname, usage=usage,
                                     description=description)

    parser.add_argument('-v', '--version', action='version',
                        help='Shows this help screen.', version=progversion)

    parser.add_argument('-C', '--config',
                        help='Reads some configurations from a file.',
                        dest='config', default=DEFAULT_CONFIG_FILE)

    args = parser.parse_args()

    return args



