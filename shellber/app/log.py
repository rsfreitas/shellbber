
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
Module to handle internal logging facility.
"""

import logging

def _translate_level(level):
    """
    A function to translate descriptive log level into the recognized level to
    the python logging module.

    :param level: The log level in a string format, such as: info, debug,
                  warning, error, etc.
    """
    return {
        'critical': logging.CRITICAL,
        'debug': logging.DEBUG,
        'error': logging.ERROR,
        'info': logging.INFO,
        'warning': logging.WARNING
    }.get(level, logging.INFO)



def start_log(filename, level):
    log_format = '%(asctime)s:%(levelname)s:%(process)s:%(module)s:%(message)s'
    msg_level = _translate_level(level)
    logging.basicConfig(filename=filename, level=msg_level,
                        format=log_format)



