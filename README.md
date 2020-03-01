# sh2msg tool

This tool helps with the translation of Silent Hill 2 game.

It has been created to be compatible with Japanese and EFGIS files, you
can fine control the text flow and this tool doesn't hide anything to
the translator.

You can download the last version of this program at [insert url here]

## Installation and requirements

You can download the binaries for windows and GNU/Linux, if you are
going to use the source code directly, you need Python >= 3.4
installed.

You can download the last version of Python 3 at https://www.python.org/

### Run the program

This is a command line only program, you need to run it inside
*Command Prompt* (or *PowerShell*) in Windows. You can use the
executable, but in case you want to go with the source code, you can
run it by typing:

```bash
python3 -m sh2msg
```

Some Python 3 installations have *python* as name of the interpreter.

## Usage

As mentioned before, this is a command line only program, you need to
be able to navigate your file-system and call the program.

You can dump the content of a .mes file into text by typing:

```bash
sh2msg common_msg_e.mes
```

the tool will detect the language from the filename and create a
*common_msg_e.txt* file.

You can run the tool against multiple files too:

```bash
sh2msg common_msg_e.mes stage_apart_stair_msg_e.mes
```

if you shell supports glob expansion:

```bash
sh2msg *.mes
```

### Load external symbol table

You can load the symbol table from an external file. You might want to
use this feature if your language cannot be expressed using the game's
default charter set.

```bash
sh2msg common_msg_e.mes --table turkish_table.txt
```

### Text files explained

The text will look something like this:

```
--------------- strings=42 language=english
---------------
Nice tool!
        Yeah I can finally edit the strings without pain...<SEPARATORB>
---------------
We should build a statue.
        You are right...<SEPARATORB>
---------------
It's too dark to tell for sure, but I
        think there's something on the
[...more text...]
```

The first line is the *header* and should not be touched by the
translator, it's used by the tool for checking the results of the
final .mes file.

Every string is separated by 15 dashes, inside a string we might have
some control codes like `<SEPARATORB>`. You need to keep those codes
in other to make the translation work.

There is a list of knows codes the source repository in
`sh2msg/table/data`.

### Newlines and new pages

In the previous example, can you see the tabs in the beginning of the
line? If a line starts with a TAB the tool will place a NEWLINE code
in the game files!

If you place an empty line, you will have a NEWPAGE. It's recommended
to use a text editor where tabs and space are highlight.

### Raw mode

You can dump and insert in RAW mode, the text file produces contains a
string for every line and every char is inserted into a .mes file
without any check. Use this mode carefully.

## Changelog

1.6 Accept multiple files as input, bugfix on external tables

1.5 Better error handling

1.0 Internal first release

## Copyright

sh2msg-convert is for editing game files for silent hill 2 game

Copyright © 2019 Gianluigi "Infrid" Cusimano, Víctor "IlDucci" González

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
