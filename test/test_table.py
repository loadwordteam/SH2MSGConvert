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
import collections
from .context import sh2msg
from .context import TEST_DATA_DIR


class TestTableWrongDigit(unittest.TestCase):
    def test(self):
        self.assertRaises(sh2msg.table.TableException,
                          sh2msg.table.parse_table,
                          '''
                          336699=B
                          3322KK=C
                          ''')


class TestTableUnevenHex(unittest.TestCase):
    def test(self):
        self.assertRaises(sh2msg.table.TableException,
                          sh2msg.table.parse_table,
                          '''
                          336699=B
                          11111=K
                          ''')


class TestTableNoEqual(unittest.TestCase):
    def test(self):
        self.assertRaises(sh2msg.table.TableException,
                          sh2msg.table.parse_table,
                          '''
                          336699B
                          ''')


class TestTableParse(unittest.TestCase):
    def test(self):
        self.assertEqual(
            sh2msg.table.parse_table(
                '''
                99=B
                00=K
                '''),
            collections.OrderedDict(
                [(b'\x99', 'B'), (b'\x00', 'K')]
            )
        )


class TestTableParseFlip(unittest.TestCase):
    def test(self):
        self.assertEqual(
            sh2msg.table.parse_table(
                '''
                99=B
                00=K
                ''', flip=True),
            collections.OrderedDict(
                [('B', b'\x99'), ('K', b'\x00')]
            )
        )


class TestLoadSomeTable(unittest.TestCase):
    def test(self):
        filename = os.path.join(TEST_DATA_DIR, 'sample.tbl')

        self.assertIsInstance(
            sh2msg.table.read_table_file(filename),
            collections.OrderedDict
        )
        self.assertIsNotNone(
            sh2msg.table.read_table_file(filename),
        )


class TestLoadDefaultTable(unittest.TestCase):
    def test(self):
        self.assertIsInstance(
            sh2msg.table.load_default_table(),
            collections.OrderedDict
        )
        self.assertIsNotNone(
            sh2msg.table.load_default_table()
        )
