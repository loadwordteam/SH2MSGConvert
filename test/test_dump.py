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

import unittest
import os
from .context import TEST_DATA_DIR

from sh2msg import read_container
from sh2msg.table.parse import load_default_table


class TestBasicDump(unittest.TestCase):
    def test(self):
        self.maxDiff = 9999
        mes_data = read_container(
            os.path.join(TEST_DATA_DIR, 'dante_ok.mes'),
            load_default_table()
        )

        mes_data = [line.rstrip() for line in mes_data.split("\n")]
        mes_data = "\n".join(mes_data)

        dante_text = None
        with open(os.path.join(TEST_DATA_DIR, 'dante.txt')) as dante:
            dante_text = "\n".join([x.rstrip() for x in dante.readlines()])

        self.assertEqual(mes_data, dante_text)
