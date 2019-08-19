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
import tempfile
from .context import TEST_DATA_DIR

from sh2msg import read_container, pack_container, dump_container
from sh2msg.table.parse import load_default_table


class TestReadContainer(unittest.TestCase):
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


class TestDumpNoClean(unittest.TestCase):
    def test(self):
        self.maxDiff = 9999

        temp_mes = tempfile.NamedTemporaryFile(prefix='sh2mgs_test_')
        temp_text = tempfile.NamedTemporaryFile(prefix='sh2mgs_test_text_')

        pack_container(
            temp_mes.name,
            os.path.join(TEST_DATA_DIR, 'carducci_raw.txt'),
            load_default_table(flip=True),
            clean_mode=False
        )

        dump_container(
            temp_mes.name,
            temp_text.name,
            table=load_default_table(),
            clean_mode=False
        )

        with open(temp_text.name, 'r', encoding="utf-8-sig") as f_text, open(
                os.path.join(TEST_DATA_DIR, 'carducci_raw.txt'), 'r', encoding="utf-8-sig") as f_carducci:
            test_text = "\n".join([line.rstrip() for line in f_text.read().split("\n")])
            carducci = f_carducci.read()
            self.assertEqual(test_text.rstrip(), carducci.rstrip())


class TestDumpCleanMode(unittest.TestCase):
    def test(self):
        self.maxDiff = 9999

        temp_mes = tempfile.NamedTemporaryFile(prefix='sh2mgs_test_')
        temp_text = tempfile.NamedTemporaryFile(prefix='sh2mgs_test_text_')

        pack_container(
            temp_mes.name,
            os.path.join(TEST_DATA_DIR, 'carducci_raw.txt'),
            load_default_table(flip=True),
            clean_mode=False
        )

        dump_container(
            temp_mes.name,
            temp_text.name,
            table=load_default_table(),
            clean_mode=True
        )

        with open(temp_text.name, 'r', encoding="utf-8-sig") as f_text, open(
                os.path.join(TEST_DATA_DIR, 'carducci_clean.txt'), 'r', encoding="utf-8-sig") as f_carducci:
            test_text = "\n".join([line.rstrip() for line in f_text.read().split("\n")])
            carducci = f_carducci.read()
            self.assertEqual(test_text.rstrip(), carducci.rstrip())
