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

import os

import sys
from pathlib import Path

basedir = None

# fix for windows build
if getattr(sys, 'frozen', False):
    basedir = Path(sys._MEIPASS).joinpath('sh2msg', 'table')
else:
    basedir = Path(__file__).parent

DEFAULT_TABLE_PATH = basedir.joinpath('data', 'table.txt').resolve()
JAP_TABLE_PATH = basedir.joinpath('data', 'tableJAP.txt').resolve()

from sh2msg.table.parse import TableException
from sh2msg.table.parse import parse_table
from sh2msg.table.parse import read_table_file
from sh2msg.table.parse import load_default_table
from sh2msg.table.parse import load_jap_table
from sh2msg.table.parse import get_language_from_path
