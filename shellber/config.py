
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
import commentjson as json

def load(args):
    """
    """
    if args.config is None:
        filename = args.config
    else:
        filename = ''

    with open(filename) as fd:
        data = fd.read()

    # Are we reading a JSON file?
    try:
        cfg = json.loads(data)
    except json.JSONLibraryException:
        # Or is it a YAML file?
        try:
            cfg = yaml.load(data)
        except yaml.YAMLError:
            return False

    return True



