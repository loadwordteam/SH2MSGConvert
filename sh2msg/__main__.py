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
import sys

from sh2msg import pack_container, TableException, MesNotValid
from sh2msg import dump_container
import sh2msg.table
from sh2msg.cli import parse
from sh2msg import check_mes_structure
from sh2msg.dump import MesDumpException
from sh2msg.insert import MesInsertException
from sh2msg.table import get_language_from_path
from sh2msg.header import parse_header, parse_header_from_file, HeaderException

if __name__ == '__main__':
    args = parse.parser.parse_args()
    try:
        out_base_dir = None
        if args.output and len(args.files) > 1:
            out_base_dir = pathlib.Path(args.output)
            if out_base_dir.suffix == '.txt' or out_base_dir.suffix == '.mes':
                raise Exception("You cannot write multiple input files into the same output file")
            if not out_base_dir.is_dir():
                raise Exception("When you provide multiple files as input, you must create the output directory '{}' first".format(out_base_dir.resolve()))

        file_list = args.files or parse.read_file_list(args.file_list)
        for input_file in file_list:
            message = pathlib.Path(input_file)
            table = None
            # this is a flag for telling to the table to use the chars as key
            flip = bool(message.suffix == '.txt')
            clean_mode = not args.raw_mode
            language = None

            out_path = None

            if out_base_dir:
                out_path = out_base_dir.joinpath(message.name)

            if args.table is None:
                if args.table_jpn:
                    table = sh2msg.table.load_jpn_table(flip=flip)
                else:
                    language = get_language_from_path(message)
                    table = sh2msg.table.load_default_table(flip=flip, language=language)
            else:
                table = sh2msg.table.read_table_file(args.table, flip=flip)

            if message.suffix == '.mes' and check_mes_structure(message.resolve()):
                dump_container(message.resolve(),
                               out_path.with_suffix('.txt').resolve() if out_path else message.with_suffix('.txt').resolve(),
                               table=table,
                               clean_mode=clean_mode)
            elif message.suffix == '.txt':
                num_strings = None
                if clean_mode:
                    language, num_strings = parse_header_from_file(message)
                    if language and args.table is None:
                        table = sh2msg.table.load_default_table(flip=flip, language=language)
                pack_container(
                    out_path.with_suffix('.mes').resolve() if out_path else message.with_suffix('.mes').resolve(),
                    message.resolve(),
                    table=table,
                    clean_mode=clean_mode,
                    num_line_check=num_strings,
                    language=language)
    except TableException as exp:
        print('[ERROR Table] {}'.format(exp), file=sys.stderr)
    except HeaderException as exp:
        print('[ERROR Parse header in txt] {}'.format(exp), file=sys.stderr)
    except MesInsertException as exp:
        print('[ERROR Insert in .mes file] {}'.format(exp), file=sys.stderr)
    except MesNotValid as exp:
        print('[ERROR .mes is not valid] {}'.format(exp), file=sys.stderr)
    except MesDumpException as exp:
        print('[ERROR Dump .mes] {}'.format(exp), file=sys.stderr)
    except Exception as exp:
        print('[UNEXPECTED ERROR] {}'.format(exp), file=sys.stderr)
