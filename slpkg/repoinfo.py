#!/usr/bin/python
# -*- coding: utf-8 -*-

# repoinfo.py file is part of slpkg.

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
import sys

from repositories import Repo
from sizes import units
from repolist import RepoList
from __metadata__ import (
    default_repositories,
    lib_path,
    log_path,
    repositories,
    color
)


class RepoInfo(object):

    def __init__(self):
        self.form = {
            'Last updated:': '',
            'Number of packages:': '',
            'Repo id:': '',
            'Default:': '',
            'Repo url:': '',
            'Status:': '',
            'Total compressed packages:': '',
            'Total uncompressed packages:': ''
        }

        self.all_repos = RepoList().all_repos
        self.all_repos.update(Repo().custom_repository())
        del RepoList().all_repos

    def view(self, repo):
        '''
        View repository information
        '''
        status = '{0}disabled{1}'.format(color['RED'], color['ENDC'])
        self.form['Status:'] = status
        self.form['Default:'] = 'no'
        if repo in default_repositories:
            self.form['Default:'] = 'yes'
        if (repo in repositories and
                os.path.isfile(lib_path + '{0}_repo/PACKAGES.TXT'.format(
                    repo))):
            status = '{0}enabled{1}'.format(color['GREEN'], color['ENDC'])
            if repo != 'sbo':
                data = self.repository_data(repo)
                size = units(data[1], data[2])
                self.form['Repo id:'] = repo
                self.form['Repo url:'] = self.all_repos[repo]
                self.form['Total compressed packages:'] = '{0} {1}'.format(
                    str(size[1][0]), str(size[0][0]))
                self.form['Total uncompressed packages:'] = '{0} {1}'.format(
                    str(size[1][1]), str(size[0][1]))
                self.form['Number of packages:'] = data[0]
                self.form['Status:'] = status
                self.form['Last updated:'] = data[3]
        elif (repo == 'sbo' and os.path.isfile(lib_path + '{0}_repo/'
                                               'SLACKBUILDS.TXT'.format(repo))):
            status = '{0}enabled{1}'.format(color['GREEN'], color['ENDC'])
            sum_sbo_pkgs = 0
            for line in open(lib_path + 'sbo_repo/SLACKBUILDS.TXT', 'r'):
                if line.startswith('SLACKBUILD NAME: '):
                    sum_sbo_pkgs += 1
            with open(log_path + 'sbo/ChangeLog.txt', 'r') as changelog_txt:
                last_upd = changelog_txt.readline().replace('\n', '')
            self.form['Repo id:'] = repo
            self.form['Repo url:'] = self.all_repos[repo]
            self.form['Total compressed packages:'] = ''
            self.form['Total uncompressed packages:'] = ''
            self.form['Number of packages:'] = sum_sbo_pkgs
            self.form['Status:'] = status
            self.form['Last updated:'] = last_upd
        print('')
        for key, value in sorted(self.form.iteritems()):
            print color['GREY'] + key + color['ENDC'], value
        print('')
        sys.exit(0)

    def repository_data(self, repo):
        '''
        Grap data packages
        '''
        sum_pkgs, size, unsize, last_upd = 0, [], [], ''
        for line in open(lib_path + repo + '_repo/PACKAGES.TXT', 'r'):
            if line.startswith('PACKAGES.TXT;'):
                last_upd = line[14:].strip()
            if line.startswith('PACKAGE NAME:'):
                sum_pkgs += 1
            if line.startswith('PACKAGE SIZE (compressed):  '):
                size.append(line[28:-2].strip())
            if line.startswith('PACKAGE SIZE (uncompressed):  '):
                unsize.append(line[30:-2].strip())
        if repo in ['salix', 'slackl']:
            with open(log_path + '{0}/ChangeLog.txt'.format(repo), 'r') as log:
                last_upd = log.readline().replace('\n', '')
        return [sum_pkgs, size, unsize, last_upd]
