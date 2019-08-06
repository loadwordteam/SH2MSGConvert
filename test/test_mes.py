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
from .context import sh2msg
from .context import TEST_DATA_DIR


class MesFileNotFound(unittest.TestCase):
    def test(self):
        self.assertRaises(
            sh2msg.MesFormatException,
            sh2msg.check_mes_structure,
            'file_not_found123.mes'
        )


class MesTooBig(unittest.TestCase):
    def test(self):
        tmp = tempfile.NamedTemporaryFile()
        tmp.write(b'\xff' * (1024 * 1024 + 1))
        self.assertRaises(
            sh2msg.MesFormatException,
            sh2msg.check_mes_structure,
            tmp.name
        )
        tmp.close()


class MesTooSmall(unittest.TestCase):
    def test(self):
        tmp = tempfile.NamedTemporaryFile()
        tmp.write(b'\xff' * +2)
        self.assertRaises(
            sh2msg.MesFormatException,
            sh2msg.check_mes_structure,
            tmp.name
        )
        tmp.close()


class MesTooManyEntries(unittest.TestCase):
    def test(self):
        self.assertRaises(
            sh2msg.MesNotValid,
            sh2msg.check_mes_structure,
            os.path.join(TEST_DATA_DIR, 'dante_too_many_entries.mes')
        )


class MesFirstPointerOverSize(unittest.TestCase):
    def test(self):
        self.assertRaises(
            sh2msg.MesNotValid,
            sh2msg.check_mes_structure,
            os.path.join(TEST_DATA_DIR, 'dante_first_pointer_over_size.mes')
        )


class MesPointerOverSize(unittest.TestCase):
    def test(self):
        self.assertRaises(
            sh2msg.MesNotValid,
            sh2msg.check_mes_structure,
            os.path.join(TEST_DATA_DIR, 'dante_pointer_over_size.mes')
        )


class MesPointerNotMonotone(unittest.TestCase):
    def test(self):
        self.assertRaises(
            sh2msg.MesNotValid,
            sh2msg.check_mes_structure,
            os.path.join(TEST_DATA_DIR, 'dante_not_monotone.mes')
        )


class MesValid(unittest.TestCase):
    def test(self):
        self.assertTrue(
            sh2msg.check_mes_structure,
            os.path.join(TEST_DATA_DIR, 'dante_ok.mes')
        )
