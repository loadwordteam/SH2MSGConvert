[![Docker Repository on Quay](https://quay.io/repository/loadwordteam/sh2msgconvert/status "Docker Repository on Quay")](https://quay.io/repository/loadwordteam/sh2msgconvert)
# sh2msg tool

This tool is designed to convert back and forth the .mes files from
Silent Hill 2 (PC and XBOX versions) in order to translate the game.

It has been created to be compatible with the original Japanese,
English, French, Italian, German and Spanish files, as well as the PC
Enhanced Edition modifications. Unlike other previous programs, this
one allows for precise control of the text flow and doesn't hide
anything to the translator, leaving most of the control and possible
text bug solving to them.

You can download the last version of this program at <https://github.com/loadwordteam/SH2MSGConvert/releases>

## Installation and requirements

You can just download the binaries for Windows and GNU/Linux to use
the tool. If you are going to use the source code directly, you need
Python >= 3.4 installed.

You can download the last version of Python 3 at
https://www.python.org/

### Handling the program

This is a command line only program, so you need to run it inside
*Command Prompt* (or *PowerShell*) in Windows. In case you want to
use the source code instead, you can run it by typing:

```bash
python3 -m sh2msg
```

Some Python 3 installations have *python* as name of the interpreter
instead of *python3*.

## Usage

Since this is a command line only program, you need to be able to
navigate your file system and call the program.

You can dump the content of a .mes file into text by typing:

```bash
sh2msg common_msg_e.mes
```

The tool will detect the language from the filename and create a
*common_msg_e.txt* file.

You can also run the tool against multiple files:

```bash
sh2msg common_msg_e.mes stage_apart_stair_msg_e.mes
```

If you shell supports glob expansion, type this:

```bash
sh2msg *.mes
```

### Load an external character table

You can load the character table from an external file. You will find 
this feature useful if your language uses characters that are not
within the game's default set.

Make sure you have already modified the game's font within the executable file 
(or, in the case of the Enhanced Edition, have the edited texture with the new 
characters) before changing the character table. You will need to have both 
the table and the font ready to be able to see new characters for your language.

```bash
sh2msg common_msg_e.mes --table turkish_table.txt
```

You can find tables that you can use as a base for your translation efforts
[in the table/data folder](sh2msg/table/data).

Keep in mind that if you want to translate to Asian or languages that require 
the extended Japanese sheet, you will need to use the [tableJPN.txt](sh2msg/table/data/tableJPN.txt) 
file instead of the regular one.

### Text files explanation

A text file will look something like this:

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
translator, it's used by the tool to verify the results of the final
.mes file.

Every string is separated by 15 dashes, which are used by the tool to
identify the end and beginning of each string. Do not change the
amount of dashes, or else the tool will reject the file.

Some strings contain control codes, like `<SEPARATORB>`,
`<VARIABLE-01>`, etc. You need to keep those codes in order to avoid
any unwanted issues during the game.

For more information on the known control codes, you can either check
the source repository at `sh2msg/table/data` or the Control Codes
document located in [ControlCodes.md](ControlCodes.md).

### Newlines and new pages

In the previous example, can you see the tabs in the beginning of the
line? If a line starts with a TAB, the tool will place a NEWLINE code
in the game files!

If you place an empty line, you will have a NEWPAGE. It's recommended
to use a text editor where tabs and space are highlighted.

Changing the amount of NEWLINEs and NEWPAGEs shouldn't affect the
behavior of the text files during gameplay, they can be added or 
removed at will (But handle with care).

If, like it was done in the English version of the Enhanced Edition's
changes, you want to make a page with two paragraphs, all you need to
do is to add a new line with just a tabulation.

### Raw mode

You can dump and insert .mes files in RAW mode. In this mode, the
resulting text file will contain every control code being used in the
game without any form of cleanup for non-programmers and the
insertion process will be made without any checks. Handle this mode
with care.

## Changelog

1.7 Breaking change on `--table-jap`, in case you didn't know the term _Jap_ is an ethnic slur, you can read more about it on [Wikipedia](https://en.wikipedia.org/wiki/Jap). Now the switch has been changed to `--table-jpn`.

1.6 Accept multiple files as input, bugfix on external tables

1.5 Better error handling

1.0 Internal first release

## Copyright

sh2msg-convert is a text conversion tool for Silent Hill 2.

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


## Contacts

Gianluigi "Infrid" Cusimano <infrid@infrid.com>

https://loadwordteam.com/

[![a project by load word team](https://loadwordteam.com/logo-lwt-small.png "a project by load word team")](https://loadwordteam.com)

