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

import pathlib

from sh2msg import pack_container
from sh2msg import dump_container
import sh2msg.table
from sh2msg.cli import parse
from sh2msg import check_mes_structure

if __name__ == '__main__':
    args = parse.parser.parse_args()

    message = pathlib.Path(args.filename)
    table = None
    flip = bool(message.suffix == '.txt')

    if args.table is None:
        if args.table_jap:
            table = sh2msg.table.load_jap_table(flip=flip)
        else:
            table = sh2msg.table.load_default_table(flip=flip)
    else:
        table = sh2msg.table.read_table_file(args.table, flip=flip)

    clean_mode = not args.raw_mode
    if message.suffix == '.mes' and check_mes_structure(message.resolve()):
        dump_container(message.resolve(), args.output or message.with_suffix('.txt').resolve(), table=table, clean_mode=clean_mode)
    elif message.suffix == '.txt':
        pack_container(args.output or message.with_suffix('.mes').resolve(), message.resolve(), table=table, clean_mode=clean_mode)
