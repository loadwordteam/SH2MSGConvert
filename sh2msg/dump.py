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


class MesDumpException(Exception):
    pass


def filter_clean_dump(text):
    cleaner = re.compile(r'(?:<SEPARATORA>)?(.+?)(?:<STRING-END>)?(?: ?<SEPARATORA>)?(<SEPARATORB>)?')

    output = [
        (cleaner.sub(r'\1\2', line)).replace("<NEWLINE>", "\n\t ") for line in text.split("\n")
    ]
    return "\n".join(output)


def read_container(path, table={}):
    path = pathlib.Path(path)
    if not path.is_file():
        raise MesDumpException('Cannot read {}'.format(path.resolve()))
    found_strings = []
    with path.open('br') as container:
        entries = int.from_bytes(container.read(2), 'little')

        pointers = []
        for idx in range(entries):
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
        return "\n".join(found_strings)


def dump_container(path_mes, out_txt, encoding="utf-8-sig", table={}, clean_mode=True):
    lines = read_container(path_mes, table=table)

    if clean_mode:
        lines = filter_clean_dump(lines)

    with open(out_txt, 'w', encoding=encoding) as txt_file:
        txt_file.write(lines)
