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
import itertools
import re

from sh2msg import COMMENT_FORMAT

SUPPORTED_LANGUAGES = {
    '_e': ['english', 'en'],
    '_f': ['french', 'fr'],
    '_g': ['german', 'de'],
    '_i': ['italian', 'it'],
    '_j': ['japanese', 'ja']
}

CONF_LANGUAGE = 'language'
CONF_NUM_LINES = 'lines'


class HeaderException(Exception):
    pass


def parse_header(text):
    if text.find(CONF_LANGUAGE) == -1 and text.find(CONF_NUM_LINES) == -1:
        return None, None

    num_lines = None
    language = None

    for conf in re.findall('([a-z]+ *= *[^ ]+ *)', text):
        key, value = conf.split('=')
        value = value.strip()
        if key == CONF_NUM_LINES:
            try:
                num_lines = int(value)
            except ValueError:
                raise HeaderException('Value for lines {} invalid, expected numeric'.format(value))
        elif key == CONF_LANGUAGE:

            all_languages = dict(
                itertools.chain.from_iterable(
                    (
                        (
                            (x[1][0], x[0]), (x[1][1], x[0])
                        ) for x in SUPPORTED_LANGUAGES.items()
                    )
                )
            )

            if all_languages.get(value.lower(), None):
                language = all_languages.get(value.lower())
            else:
                raise HeaderException('Value for language {} invalid expected one of the following: {}'.format(
                    value,
                    ", ".join(all_languages.keys()))
                )
        else:
            raise HeaderException(
                'Configuration not valid, found "{}", expected "{}" or "{}"'.format(key, CONF_LANGUAGE, CONF_NUM_LINES)
            )

    return language, num_lines


def make_header(language, num_lines):
    return "{} language={} lines={}".format(COMMENT_FORMAT, language, num_lines)
