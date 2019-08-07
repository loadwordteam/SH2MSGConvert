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

DEFAULT_TABLE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './data/table.txt'))
JAP_TABLE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './data/tableJAP.txt'))

from sh2msg.table.parse import TableException
from sh2msg.table.parse import parse_table
from sh2msg.table.parse import read_table_file
from sh2msg.table.parse import load_default_table
from sh2msg.table.parse import load_jap_table
