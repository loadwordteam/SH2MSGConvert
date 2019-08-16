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


class MesInsertException(Exception):
    pass


def filter_cleaned_text(text_data):
    """This function expects lines to be a multiline string, the newline char assumed
    is \n, the conversion from Windows/Mac style can be done during the file read!"""

    newline_re = re.compile(r'^[\t ]+(.*)')
    output = []
    for line in text_data.split("\n"):
        if line.startswith('--') or not line.strip():
            continue
        newline = newline_re.findall(line)
        if newline:
            for find in newline:
                output.append("<NEWLINE>" + find.rstrip())
        else:
            output.append(line.rstrip())

    output = "\n".join(output).replace("\n<NEWLINE>", "<NEWLINE>")

    output = [
        "<SEPARATORA>{0}<STRING-END>{1}".format(
            x.replace('<SEPARATORB>', ''),
            '<SEPARATORB>' if x.endswith('<SEPARATORB>') else '<SEPARATORA>'
        ) for x in output.split("\n")
    ]

    space_between = re.compile(r'(<[a-z1-2\-]+>)([ \t]+)(<[a-z1-2\-]+>)', re.IGNORECASE)

    # remove space among control sequences
    output = [space_between.sub(r'\1\3', x) for x in output]

    return "\n".join(output)


def pack_container(path_mes, path_txt, table, encoding="utf-8-sig", clean_mode=False):
    with open(path_mes, 'bw') as container, open(path_txt, "r", encoding=encoding) as text_data:
        binary_lines = []
        text_data = text_data.read()

        if clean_mode:
            text_data = filter_cleaned_text(text_data)

        for line_number, line in enumerate(text_data.split("\n")):
            string = line.rstrip()
            if string:
                full_string_len = len(string)
                encoded_pairs = []
                start = end = 0
                while start <= full_string_len - 1:
                    for value, hex_code in table.items():
                        end = start + len(hex_code)
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
                line_length = sum(len(hex_code) for value, hex_code in encoded_pairs)
                if line_length % 2 != 0:
                    # let's pad the line
                    last_value, last_code = encoded_pairs[-1]
                    if last_value[0] == '<' and last_value[-1] == '>':
                        encoded_pairs[-1] = (' ', b'\x00')
                        encoded_pairs.append((last_value, last_code))
                    else:
                        encoded_pairs.append((' ', b'\x00'))

                binary_lines.append(b''.join([code for value, code in encoded_pairs]))
        start_offset = 2 + len(binary_lines) * 2

        pointers = [start_offset, ]
        for idx, string in enumerate(binary_lines[:-1]):
            pointers.append(
                int(
                    (len(string) + pointers[idx])
                )
            )

        pointers = [struct.pack('<H', int(data / 2)) for data in pointers]
        container.write(struct.pack('<H', len(binary_lines)))
        container.write(b''.join(pointers))
        container.write(b''.join(binary_lines))
