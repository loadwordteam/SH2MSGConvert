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


from setuptools import setup, find_packages

from sh2msg import VERSION_NUMBER

with open('README.rst') as f:
    readme = f.read()

with open('COPYING') as f:
    license = f.read()

setup(
    name='sh2msg',
    version=VERSION_NUMBER,
    description='sh2msg-convert is a text conversion tool for Silent Hill 2',
    long_description=readme,
    author='Gianluigi "Infrid" Cusimano, Víctor "IlDucci" González',
    author_email='infrid@infrid.com',
    url='https://gitlab.com/sh2msgconvert',
    license=license,
    packages=find_packages(exclude=('test', 'docs')),
    install_requires=[],
)
