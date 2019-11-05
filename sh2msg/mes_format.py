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

import struct
import pathlib
import os

MAX_MES_SIZE = 1024 * 1024


class MesNotValid(Exception):
    pass


def check_mes_structure(mes_filename):
    """Runs some empirical checks on the .mes format, we can't rely just
    on the filename, we meed to check the structure."""
    mes_path = pathlib.Path(mes_filename)

    if not mes_path.is_file():
        raise MesNotValid('file {} does not exist'.format(mes_path.resolve()))

    filesize = mes_path.stat().st_size
    if filesize > MAX_MES_SIZE:
        raise MesNotValid('file {} is too big (> 1MB)'.format(mes_path.resolve()))

    if filesize < 6:
        raise MesNotValid(
            'file {} is too small only {} bytes'.format(mes_path.resolve(), mes_path.stat().st_size))

    with mes_path.open(mode='rb') as container:
        strings = int.from_bytes(container.read(2), 'little')
        if strings * 2 >= filesize - 2:
            raise MesNotValid('file {}: number of strings exceeded the file itself'.format(mes_path.resolve()))
        pointer = int.from_bytes(container.read(2), 'little') * 2
        if pointer >= filesize:
            raise MesNotValid('file {}: pointer goes over the file size'.format(mes_path.resolve()))

        if strings > 1:
            for idx in range(strings - 1):
                next_pointer = int.from_bytes(container.read(2), 'little') * 2
                if next_pointer >= filesize:
                    raise MesNotValid('file {}: pointer goes over the file size'.format(mes_path.resolve()))
                if next_pointer <= pointer:
                    raise MesNotValid('file {}: pointers are not monotonically increasing'.format(mes_path.resolve()))
                pointer = next_pointer

    return True
