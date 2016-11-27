
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

DEFAULT_LOG_FILENAME = 'shellber.log'
DEFAULT_LOG_LEVEL = 'debug'
DEFAULT_CONFIG_FILENAME = 'shellber.yml'

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



def _create_default_values(parameters):
    """
    Function to create default values to internal configurations.
    """
    parameters.log_filename = DEFAULT_LOG_FILENAME
    parameters.log_level = DEFAULT_LOG_LEVEL
    parameters.filename = DEFAULT_CONFIG_FILENAME



def load(filename):
    """
    A function to load the application config file into the memory.

    :return On success returns a ConfigParameter class with all loaded info or
            None otherwise.
    """
    cfg_options = ConfigParameters()

    try:
        with open(filename) as fd:
            data = fd.read()
    except:
        _create_default_values(cfg_options)
        return cfg_options

    cfg_options.filename = filename

    try:
        cfg = yaml.load(data)
    except yaml.YAMLError:
        _create_default_values(cfg_options)
        return cfg_options

    cfg_options.log_filename = cfg.get('log_filename')
    cfg_options.log_level = cfg.get('log_level')

    if cfg.has_key('account'):
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



def display_configurations(cfg_options):
    output = '\n'

    if cfg_options is None:
        output += 'Empty configurations'
    else:
        output += 'Log filename: ' + cfg_options.log_filename + '\n'
        output += 'Log level: ' + cfg_options.log_level + '\n'

        if hasattr(cfg_options, 'account'):
            output += '\nAccount details:\n\n'
            output += ' Username: ' + cfg_options.account['username'] + '\n'
            output += ' Password: ' + cfg_options.account['password'] + '\n'
            output += ' Server: ' + cfg_options.account['server'] + '\n'
            output += ' Service: ' + cfg_options.account['host'] + '\n'

    return output



