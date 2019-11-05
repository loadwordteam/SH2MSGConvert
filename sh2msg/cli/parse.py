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

parser = argparse.ArgumentParser(description='sh2msg v{} - Dump or insert text for Silent Hill 2 .msg files'.format(VERSION_NUMBER),
                                 epilog=HOMEPAGE)
parser.add_argument('filename', metavar='FILE', type=str,
                    help='Decode or encode a .mes or .txt file, file extensions is used to guess the file type')

parser.add_argument('--output', '-o', dest='output', type=str,
                    help='Path for the destination file, if not provided writes in the source folder with the correct extension')

parser.add_argument('--table', '-t', dest='table', type=str,
                    help='Define an alternate table file from disk, useful for testing and development')

parser.add_argument('--table-jap', '-j', dest='table_jap', action='store_true',
                    help='Force to use the Japanese table, otherwise automatically select the correct one')

parser.add_argument('--raw-mode', '-r', dest='raw_mode', action='store_true',
                    help="Read and write without cleaning or escaping the text")
