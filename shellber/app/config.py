
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

import yaml

class ConfigParameters(object):
    """
    A class to hold all application parameters loaded/written into the
    config file.
    """
    def __repr(self):
        return "ConfigParameters(data=%r)" % self.__dict__


    def __str__(self):
        return str(self.__dict__)


    def data(self):
        return self.__dict__



def load(filename):
    """
    A function to load the application config file into the memory.

    :return On success returns a ConfigParameter class with all loaded info or
            None otherwise.
    """
    try:
        with open(filename) as fd:
            data = fd.read()
    except:
        return None

    cfg_options = ConfigParameters()
    cfg_options.filename = filename

    try:
        cfg = yaml.load(data)
    except yaml.YAMLError:
        return None

    cfg_options.log_filename = cfg.get('log_filename')
    cfg_options.log_level = cfg.get('log_level')
    cfg_options.account = cfg.get('account')

    return cfg_options



def save(cfg_options):
    """
    A function to write/update the application config file with the actual
    configurations.

    :param cfg_options: A ConfigParameters object with all config info.

    :return On success returns True or False otherwise.
    """
    if isinstance(cfg_options, ConfigParameters) is False:
        return False

    with open(cfg_options.filename, 'w+') as fd:
        yaml.dump(cfg_options.data(), fd, default_flow_style=False,
                  allow_unicode=True)

    return True



