# -*- coding: utf-8 -*-
#  This file is part of sh2msg-convert.
#
#  sh2msg-convert is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  sh2msg-convert is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with sh2msg-convert.  If not, see <http://www.gnu.org/licenses/>.

import collections
import io
import string
from sh2msg.table import DEFAULT_TABLE_PATH, JAP_TABLE_PATH


class TableException(Exception):
    pass


def parse_table(table_string, flip=False):
    """Read the a Thinghy table style text file"""
    char_map = {}
    for number, line in enumerate(table_string.splitlines()):
        if line.strip():
            line_p = line.strip('\n')
            if line_p.find('=') == -1:
                raise TableException(
                    'Line malformed, does not have an = sign {}\n{}'.format(number, line)
                )

            hex_code, value = line_p.split('=', 1)
            hex_code = hex_code.strip()

            if len(hex_code) % 2 != 0:
                raise TableException(
                    'Hex digit are not even in line {}\n{}'.format(number, line)
                )

            if not all(c in string.hexdigits for c in hex_code):
                raise TableException(
                    'Hex digit invalid in line {}\n{}'.format(number, line)
                )

            byte_code = int(hex_code, 16).to_bytes(int(len(hex_code) / 2), byteorder='big')
            char_map[byte_code] = value
    keys = list(char_map.keys())
    keys.sort(key=len, reverse=True)

    if flip:
        # remove duplicates
        char_map_dup = {}
        for key, value in char_map.items():
            char_map_dup.setdefault(value, set()).add(key)

        char_map_dedup = dict(((value, min(code, key=len)) for value, code in char_map_dup.items()))
        # we put the codes first in this case
        char_codes = [key for key in char_map_dedup.keys() if key.startswith('<') and key.endswith('>')]
        char_keys = list(set(char_map_dedup.keys()) - set(char_codes))

        return collections.OrderedDict([(key, char_map_dedup[key]) for key in char_codes + char_keys])

    return collections.OrderedDict([(key, char_map[key]) for key in keys])


def read_table_file(path, flip=False, encoding="utf-8-sig"):
    table_string = ''
    with io.open(path, mode="r", encoding=encoding) as table:
        table_string = table.read()

    return parse_table(table_string, flip=flip)


def load_default_table(flip=False, encoding="utf-8-sig"):
    return read_table_file(DEFAULT_TABLE_PATH, flip=flip, encoding=encoding)


def load_jap_table(flip=False, encoding="utf-8-sig"):
    return read_table_file(JAP_TABLE_PATH, flip=flip, encoding=encoding)
