# Control Codes research

This document includes all the information we have gathered regarding
the Silent Hill 2's control codes and whether if they are simplified
or transformed by the sh2msg-convert tool.

## "-LE`>" suffix
The control code's byte endianess is swapped between the Western and
Japanese modes. Therefore, the entries for both modes are different.
Be aware of this if you're porting texts from the Japanese mode to
the Western one or vice versa.

## Common control codes

### `<CENTER-PARAGRAPH`> (Displayed)
Centers the current page to the screen, but keeping the text
left-aligned. Used mostly in Memos.

### `<CENTER-PER-LINE`> (Displayed)
Centers the current page to the screen, but keeping the text
center-aligned. Used mostly in Memos.

### `<COLOR-XXXX`> (Displayed)
Changes the color of the text. Should be pretty explanatory. Only
four colors are known and available, and the default color is WHITE.

### `<HIDDEN-TEXT`> (Displayed)
Replaces whatever text is encapsulated in two of these control codes
with a Censored-like box to hide certain elements from the player.
Used within the game to display smeared documents where some parts
are illegible or to hide certain crucial details.

### `<NEWLINE`> (Altered)
Tells the game that the current string must stop there before
proceeding to display the rest of it.

### `<SELECT-YES-OR-NO`> (Displayed)
Tells the game that the string must end with a prompt that allows the
player to choose "Yes" (Continue the action) or "No" (Cancels the
action). Do not toy with these.

### `<SEPARATORA`> (Altered)
SEPARATORA's usage is twofold. On one end, it is used as a flag to
tell the game a string that is over doesn't require a buttom press to
leave the string and return to the game.

On the other hand, if this code appears the beginning of a string or
a string section, the game will change the character encoding method
from the Japanese method (Two bytes per character) to the Western
(EFIGS) one (One byte per character, two bytes per control code,
three bytes per Japanese character, has extra padding whenever
there's two or more control codes together).

### `<SEPARATORB`> (Displayed)
Used at the end of a string to tell the game that it must wait until
the player presses a button before dissappearing. If a text
description soft locks the game, chances are the corresponding string
has the SEPARATORB missing or swapped with SEPARATORA.

### `<STRING-END`> (Altered)
Tells the game that the string is over. Must be followed by either a
`<SEPARATORA`> or `<SEPARATORB`> code.

### `<VARIABLE-XX`> (Displayed)
This control code displays a custom text imposed by the game. It can
be either a text or a numeric value. Case-dependant.

### `<WAIT`> (Altered)
Tells the game to wait for a button press to continue displaying the
current string. Is the equivalent to NEWPAGE.

### `<XOFFSET-XX`> (Displayed)
Alters the X distance between one character and the next in possibly
pixels (Using the stock 640x480 resolution?). Used only in menu
titles and certain strings from the inventory menu that are too long
in French, German and Italian.

## Unique control codes

### `<GLOBALYOFFSET-XXXX`> (Displayed)
This value is used to move string sections vertically. Since it's
only used in two specific Memo files (Tern the numbers and Born From
a Wish's board puzzle), we've added entries for these two only.

If you somehow want to tinker with the vertical positioning, you can
create new entries and change the second byte's value.

### `<LONG-LINE-PATIENTS-DIARY`> (Displayed)
Displays a long line at the end of the last page of Patient's Diary,
located in the Brookhaven's Hospital rooftop. Used exclusively in
this Memo.

### `<SELECTABLE-TEXT`> (Displayed)
Used only in Born From a Wish's board puzzle to give the player more
than two options, abandoning the limits of the "Yes"/"No" choice.

### `<TEXT-POS-XXX`> (Displayed)
We are not very sure how does this exactly works, but these strings
appear exclusively during every ending except the UFO one, during the
letter text crawl. Maybe this indicates the speed at which each
paragraph moves, maybe its position. Try to avoid touching it and/or
leaving the amount of lines per paragraph identical.

## Changelog

1.0 - First version of this document.

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
along with this program.  If not, see `<http://www.gnu.org/licenses/`>.
