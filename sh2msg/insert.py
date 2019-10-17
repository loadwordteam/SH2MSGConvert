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

import struct
import re

from sh2msg import COMMENT_FORMAT


class MesInsertException(Exception):
    pass


def filter_cleaned_text(text_data):
    """This function expects lines to be a multiline string, the newline char assumed
    is \n, the conversion from Windows/Mac style can be done during the file read!"""

    newline_re = re.compile(r'^\t+(.*)')
    output = []

    for part in text_data.split("\n" + COMMENT_FORMAT + "\n"):
        # ignore the blocks of pure comments
        if all(line.startswith(COMMENT_FORMAT) for line in part.split("\n")):
            continue
        part = part.rstrip("\n")
        if part.strip():
            block = []
            for line in part.split("\n"):
                if line.startswith(COMMENT_FORMAT):
                    continue

                if newline_re.findall(line):
                    line = newline_re.sub(r'<NEWLINE>\1', line)

                if not line:
                    line = '<STRING-END><WAIT><SEPARATORA>'

                block.append(line)
            output.append("".join(block))

    output = [
        "<SEPARATORA>{0}<STRING-END>{1}".format(
            x.replace('<SEPARATORB>', ''),
            '<SEPARATORB>' if x.endswith('<SEPARATORB>') else '<SEPARATORA>'
        ) for x in output
    ]
    return output


def pack_container(path_mes, path_txt, table, encoding="utf-8-sig", clean_mode=True, num_line_check=None):
    with open(path_mes, 'bw') as container, open(path_txt, "r", encoding=encoding) as f_text_data:

        binary_strings = []
        text_data = f_text_data.readlines()

        if clean_mode:
            text_cleaned = filter_cleaned_text("".join(text_data))
            if num_line_check and len(text_cleaned) != num_line_check:
                raise MesInsertException(
                    'Found {} strings on this TXT, expected {}'.format(num_line_check, len(text_cleaned))
                )
            text_data = text_cleaned

        for line_number, line in enumerate(text_data):
            string = line.rstrip()
            if string:
                full_string_len = len(string)
                encoded_pairs = []
                start = end = 0
                while start <= full_string_len - 1:
                    for value, hex_code in table.items():
                        end = start + len(value)
                        if value == string[start:end]:
                            encoded_pairs.append((value, hex_code))
                            start = end
                            break
                    else:
                        # loop completes normally, means we didn't find an entry
                        raise MesInsertException(
                            'ERROR {} Cannot convert text in bytes \t{}\t at line {}'.format(
                                path_txt,
                                string[start:end],
                                line_number
                            )
                        )
                pos = 0
                for idx, (value, hex_code) in enumerate(encoded_pairs):
                    if value == '<STRING-END>' and pos % 2 != 0 and encoded_pairs[idx + 1][0].startswith('<') and \
                            encoded_pairs[idx + 1][0].endswith('>'):
                        encoded_pairs.insert(idx + 1, (' ', table[' ']))
                    pos += len(hex_code)

                line_length = sum(len(hex_code) for value, hex_code in encoded_pairs)
                if line_length % 2 != 0:
                    # let's pad the line
                    for idx, (value, code) in reversed(list(enumerate(encoded_pairs))):
                        if not (value.startswith('<') and value.endswith('>')) and value != ' ':
                            encoded_pairs.insert(idx + 1, (' ', table[' ']))
                            break

                binary_strings.append(b''.join([code for value, code in encoded_pairs]))

        start_offset = 2 + len(binary_strings) * 2

        pointers = [start_offset, ]
        for idx, string in enumerate(binary_strings[:-1]):
            pointers.append(
                int(
                    (len(string) + pointers[idx])
                )
            )

        pointers = [struct.pack('<H', int(data / 2)) for data in pointers]
        container.write(struct.pack('<H', len(binary_strings)))
        container.write(b''.join(pointers))
        container.write(b''.join(binary_strings))
