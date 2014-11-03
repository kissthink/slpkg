#!/usr/bin/python
# -*- coding: utf-8 -*-

# mirrors.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

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


class Repo(object):

    def __init__(self):
        pass

    def slack(self):
        '''
        Official slackware repository
        '''
        return "http://mirrors.slackware.com/slackware/"

    def sbo(self):
        '''
        SlackBuilds.org repository
        '''
        return "http://slackbuilds.org/slackbuilds/"

    def rlw(self):
        '''
        Robby's repoisitory
        '''
        return "http://rlworkman.net/pkgs/"

    def alien(self):
        '''
        Alien repository
        '''
        return "http://www.slackware.com/~alien/slackbuilds/"

    def slacky(self):
        '''
        Slacky.eu repository
        '''
        return "http://repository.slacky.eu/"
