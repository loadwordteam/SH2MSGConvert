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

COMMENT_LENGHT = 15

from sh2msg.table import read_table_file
from sh2msg.table import parse_table

from sh2msg.mes_format import check_mes_structure

from sh2msg.table import TableException
from sh2msg.mes_format import MesFormatException
from sh2msg.mes_format import MesNotValid

from sh2msg.dump import dump_container, read_container, filter_clean_dump
from sh2msg.insert import pack_container, filter_cleaned_text

VERSION_NUMBER = '1.4'
