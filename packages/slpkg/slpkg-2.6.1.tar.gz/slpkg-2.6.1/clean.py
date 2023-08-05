#!/usr/bin/python
# -*- coding: utf-8 -*-

# clean.py file is part of slpkg.

# Copyright 2014-2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
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
import shutil


class Clean(object):
    """Clean all data like man page, log files, PACKAGES.TXT and
    configuration files. This is useful if "slpkg" installed via
    "pip" because pip uninstalls only Python packages and script
    and not data. So if uninstall "# pip uninstall slpkg" after run
    "# python clean.py" to remove all data and configuration file.
    keep this script if you want to remove data some time.
    NOTE: Run this script as root."""
    def __init__(self):
        self.files = [
            "/usr/man/man8/slpkg.8.gz",
            "/etc/bash_completion.d/slpkg.bash-completion",
            "/etc/fish/completions/slpkg.fish"
        ]
        self.dirs = [
            "/etc/slpkg/",
            "/var/log/slpkg/",
            "/var/lib/slpkg/",
            "/tmp/slpkg/"
        ]

    def start(self):
        for f in self.files:
            if os.path.isfile(f):
                print("Remove file --> {0}".format(f))
                os.remove(f)
        for d in self.dirs:
            if os.path.exists(d):
                print("Remove directory --> {0}".format(d))
                shutil.rmtree(d)

if __name__ == "__main__":
    Clean().start()
