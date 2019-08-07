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

parser = argparse.ArgumentParser(description='Dump or insert data.')
parser.add_argument('filename', metavar='FILE', type=str,
                    help='Decode or encode a .mes/.txt file')

parser.add_argument('--output', '-o', dest='output', type=str,
                    help='specific output file')

parser.add_argument('--table', '-t', dest='table', type=str,
                    help='define alternate table')