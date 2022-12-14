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

import argparse
from sh2msg import VERSION_NUMBER, HOMEPAGE


def read_file_list(path_list, encoding="utf-8-sig"):
    file_list = None
    with open(path_list, "r", encoding=encoding) as f_list_data:
        file_list = [f.strip() for f in f_list_data.readlines() if f.strip()]
    return file_list


parser = argparse.ArgumentParser(
    description='sh2msg v{} - Dump or insert text for Silent Hill 2 .mes files'.format(VERSION_NUMBER),
    epilog=HOMEPAGE)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('files', metavar='FILE', type=str, nargs='*', default=[],
                   help='Decode a .mes file or encode a .txt file. The file extension will be used to guess the file type.')

group.add_argument('--file-list', '-l', dest='file_list', type=str,
                   help='Process a set of files contained in a list.')

parser.add_argument('--output', '-o', dest='output', type=str,
                    help='Path for the destination file. In case it is not provided, the tool will use the source folder and change extensions accordingly.')

parser.add_argument('--table', '-t', dest='table', type=str,
                    help='Define an alternate table file from disk. Useful for testing, development and usage for any non-EFIGS languages.')

parser.add_argument('--table-jpn', '-j', dest='table_jpn', action='store_true',
                    help='Forces the Japanese table as the character encoding table, otherwise the tool will automatically select the correct one.')

parser.add_argument('--raw-mode', '-r', dest='raw_mode', action='store_true',
                    help="Read and write without cleaning or escaping the text.")
