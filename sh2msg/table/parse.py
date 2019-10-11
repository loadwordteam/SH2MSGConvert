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
import re
import pathlib
import string
import itertools
from sh2msg import COMMENT_LENGHT
from sh2msg.table import DEFAULT_TABLE_PATH, JAP_TABLE_PATH

SUPPORTED_LANGUAGES = {
    '_e': ['english', 'en'],
    '_f': ['french', 'fr'],
    '_g': ['german', 'de'],
    '_i': ['italian', 'it'],
    '_j': ['japanese', 'ja']
}


class TableException(Exception):
    pass


class HeaderNorValue(Exception):
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


def load_default_table(flip=False, encoding="utf-8-sig", language_code='_e'):
    return read_table_file(
        JAP_TABLE_PATH if language_code == '_j' else DEFAULT_TABLE_PATH,
        flip=flip,
        encoding=encoding
    )


def load_jap_table(flip=False, encoding="utf-8-sig"):
    return read_table_file(JAP_TABLE_PATH, flip=flip, encoding=encoding)


def get_language_from_path(path):
    path = pathlib.Path(path)
    if path.stem[-2:] in SUPPORTED_LANGUAGES.keys():
        return SUPPORTED_LANGUAGES[path.stem[-2:]]
    return SUPPORTED_LANGUAGES['_e']


def parse_header(text):
    PATTERN_CONF = r'-' * COMMENT_LENGHT + r'  *(lang *= *([a-z]+)|lines *= *([0-9]+))'
    re_conf = re.compile(PATTERN_CONF)
    all_langs = dict(
        itertools.chain.from_iterable(
            (
                (
                    (x[1][0], x[0]), (x[1][1], x[0])
                ) for x in SUPPORTED_LANGUAGES.items()
            )
        )
    )
    num_lines = None
    language = None
    if re_conf.match(text):
        for pattern, lang, lines in re_conf.findall(text):
            if lines:
                num_lines = int(lines.strip())
            if all_langs.get(lang.lower(), None):
                language = all_langs.get(lang.lower())
        if language is None:
            raise HeaderNorValue('Cannot recognize language')
        if (num_lines is None or language is None) and (text.find('lang') != -1 or text.find('lines') != -1):
            raise HeaderNorValue('Malformed header, check the first line!')
    return language, num_lines
