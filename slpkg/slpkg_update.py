#!/usr/bin/python
# -*- coding: utf-8 -*-

# slpkg_update.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import re
import sys
import tarfile
import subprocess

from checksum import check_md5
from grep_md5 import pkg_checksum
from url_read import URL
from downloader import Download
from __metadata__ import (
    __all__,
    __version__,
    __author__,
    default_answer,
    build_path
)


def it_self_update():
    '''
    Check from GitHub slpkg repository if new version is available
    download and update itself
    '''
    __new_version__ = ""
    repository = 'github'
    branch = 'master'
    ver_link = ('https://raw.{0}usercontent.com/{1}/{2}/'
                '{3}/{4}/__metadata__.py'.format(repository, __author__,
                                                 __all__, branch, __all__))
    version_data = URL(ver_link).reading()
    for line in version_data.splitlines():
        if line.startswith('__version_info__'):
            __new_version__ = '.'.join(re.findall(r'\d+', line))
    if __new_version__ > __version__:
        if default_answer == "y":
            answer = default_answer
        else:
            print("\nNew version '{0}-{1}' is available !\n".format(
                __all__, __new_version__))
            answer = raw_input("Would you like to upgrade [Y/n]? ")
        if answer in ['y', 'Y']:
            print("")   # new line after answer
        else:
            sys.exit(0)
        dwn_link = ['https://{0}.com/{1}/{2}/archive/'
                    'v{3}.tar.gz'.format(repository, __author__, __all__,
                                         __new_version__)]
        Download(build_path, dwn_link).start()
        os.chdir(build_path)
        slpkg_tar_file = 'v' + __new_version__ + '.tar.gz'
        tar = tarfile.open(slpkg_tar_file)
        tar.extractall()
        tar.close()
        file_name = '{0}-{1}'.format(__all__, __new_version__)
        os.chdir(file_name)
        check_md5(pkg_checksum(slpkg_tar_file[1:], "slpkg"),
                  build_path + slpkg_tar_file)
        subprocess.call('chmod +x {0}'.format('install.sh'), shell=True)
        subprocess.call('sh install.sh', shell=True)
    else:
        print('\n{0}: There is no new version, already used the last !'
              '\n'.format(__all__))
    sys.exit(0)
