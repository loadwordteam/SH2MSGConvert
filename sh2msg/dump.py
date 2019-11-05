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

import pathlib
import os
import re
from sh2msg import COMMENT_FORMAT
from sh2msg.header import make_header
from sh2msg.table import get_language_from_path


class MesDumpException(Exception):
    pass


def filter_clean_dump(strings, num_strings=None, language=None):
    """In clean mode the translator doesn't have to deal with every
    the control code for the text flow. A cleaner txt file is
    produced with nice separators for the strings."""
    output = []

    if num_strings or language:
        output.append(make_header(language[0], num_strings))

    # might not be the most elegant way
    end_strings = {
        '<STRING-END> <SEPARATORA>': '',
        '<STRING-END><SEPARATORA>': '',
        '<STRING-END> <SEPARATORB>': '<SEPARATORB>',
        '<STRING-END><SEPARATORB>': '<SEPARATORB>'
    }

    re_page = re.compile(r'<STRING-END> *<WAIT> *<SEPARATORA>')

    for idx, line in enumerate(strings):
        if line.startswith('<SEPARATORA>'):
            line = line[len('<SEPARATORA>'):]

        for find, replace in end_strings.items():
            if line.endswith(find):
                line = line[0:-len(find)] + replace
        line = line.replace("<NEWLINE>", "\n\t")
        line = re_page.sub("\n\n", line)
        output.append(line)

    return ("\n" + COMMENT_FORMAT + "\n").join(output)


def read_container(path, table={}):
    """Read the .mes file"""
    path = pathlib.Path(path)
    if not path.is_file():
        raise MesDumpException('Cannot read {}'.format(path.resolve()))
    found_strings = []
    strings = None
    language = get_language_from_path(path)
    with path.open('br') as container:
        strings = int.from_bytes(container.read(2), 'little')

        pointers = []
        for idx in range(strings):
            pointers.append(int.from_bytes(container.read(2), 'little') * 2)

        for idx, addr in enumerate(pointers):
            size = pointers[idx + 1] - pointers[idx] if idx + 1 < len(pointers) else os.path.getsize(path)
            container.seek(addr)
            string = container.read(size)
            full_string_len = len(string)
            decoded_string = ''
            start = end = 0
            while start <= full_string_len - 1:
                for code, value in table.items():
                    end = start + len(code)
                    if code == string[start:end]:
                        decoded_string += value
                        start = end
                        break
                else:
                    # loop completes normally, means we didn't find an entry
                    raise MesDumpException(
                        'ERROR {} Unknown bytes \t{}address\t{}'.format(
                            path.resolve(),
                            "".join("%02X " % b for b in string[start:end]),
                            addr + start)
                    )

            found_strings.append(decoded_string)
        return language, strings, found_strings


def dump_container(path_mes, out_txt, encoding="utf-8-sig", table={}, clean_mode=True):
    """Dump the content of a .mes file to a .txt"""
    language, num_strings, strings = read_container(path_mes, table=table)

    if clean_mode:
        strings = filter_clean_dump(strings, num_strings, language)
    else:
        strings = "\n".join(strings)

    with open(out_txt, 'w', encoding=encoding) as txt_file:
        txt_file.write(strings)
