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
import tempfile
import os
import hashlib
from .context import TEST_DATA_DIR

from sh2msg import pack_container, read_container
from sh2msg.table.parse import load_default_table
from sh2msg.insert import filter_cleaned_text


class BasicEncodingClean(unittest.TestCase):

    def test(self):
        temp_mes = tempfile.NamedTemporaryFile(prefix='sh2mgs_test_')

        pack_container(
            temp_mes.name,
            os.path.join(TEST_DATA_DIR, 'dante.txt'),
            load_default_table(flip=True),
            clean_mode=True
        )

        with open(os.path.join(TEST_DATA_DIR, 'dante.txt'), 'r') as dante_f:
            mes_data = read_container(
                temp_mes.name,
                load_default_table()
            )
            dante_text = dante_f.read()
            dante_text = "\n".join([line.rstrip() for line in dante_text.split("\n")])
            mes_data = "\n".join([line.rstrip() for line in dante_text.split("\n")])
            self.assertEqual(dante_text, mes_data)

        temp_mes.close()


class BasicEncodingNoClean(unittest.TestCase):

    def test(self):
        temp_mes = tempfile.NamedTemporaryFile(prefix='sh2mgs_test_')

        pack_container(
            temp_mes.name,
            os.path.join(TEST_DATA_DIR, 'dante.txt'),
            load_default_table(flip=True),
            clean_mode=False
        )

        with open(os.path.join(TEST_DATA_DIR, 'dante_ok.mes'), 'rb') as test_mes:
            temp_mes.seek(0)
            hash_inserted = hashlib.sha256(temp_mes.read())
            hash_test = hashlib.sha256(test_mes.read())

        temp_mes.close()
        self.assertFalse(os.path.exists(temp_mes.name))
        self.assertEqual(hash_inserted.hexdigest(), hash_test.hexdigest())


class TestCleanDumpFilter(unittest.TestCase):
    def test(self):
        self.maxDiff = 9999
        leopardi = None
        cleaned = None
        with open(os.path.join(TEST_DATA_DIR, 'leopardi.txt'), mode='r', newline="\n") as leo:
            leopardi = leo.read()

        with open(os.path.join(TEST_DATA_DIR, 'leopardi_cleaned.txt'), mode='r', newline="\n") as cls:
            cleaned = cls.read()

        self.assertEqual(filter_cleaned_text(leopardi).strip(), cleaned.strip())
