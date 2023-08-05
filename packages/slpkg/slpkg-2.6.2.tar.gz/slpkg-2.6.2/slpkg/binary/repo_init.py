#!/usr/bin/python
# -*- coding: utf-8 -*-

# repo_init.py file is part of slpkg.

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

from slpkg.utils import Utils
from slpkg.repositories import Repo
from slpkg.__metadata__ import MetaData as _meta_

from slpkg.slack.mirrors import mirrors
from slpkg.slack.slack_version import slack_ver


class RepoInit(object):
    """
    Return PACKAGES.TXT and mirror by repository
    """

    def __init__(self, repo):
        self.repo = repo
        self.meta = _meta_
        self.mirror = ""

    def fetch(self):
        if self.repo in self.meta.default_repositories:
            exec("self._init_{0}()".format(self.repo))
        else:
            exec("self._init_custom()")
        self.lib = self.meta.lib_path + "{0}_repo/PACKAGES.TXT".format(
            self.repo)
        PACKAGES_TXT = Utils().read_file(self.lib)
        return PACKAGES_TXT, self.mirror

    def _init_custom(self):
        self.mirror = "{0}".format(Repo().custom_repository()[self.repo])

    def _init_slack(self):
        self.mirror = mirrors(name="", location="")

    def _init_rlw(self):
        self.mirror = "{0}{1}/".format(Repo().rlw(), slack_ver())

    def _init_alien(self):
        ver = slack_ver()
        arch = "x86"
        if os.uname()[4] == "x86_64":
            arch = "x86_64"
        if self.meta.slack_rel == "current":
            ver = self.meta.slack_rel
        self.mirror = "{0}{1}/{2}/".format(Repo().alien(), ver, arch)

    def _init_slacky(self):
        arch = ""
        if os.uname()[4] == "x86_64":
            arch = "64"
        self.mirror = "{0}slackware{1}-{2}/".format(Repo().slacky(), arch,
                                                    slack_ver())

    def _init_studio(self):
        arch = ""
        if os.uname()[4] == "x86_64":
            arch = "64"
        self.mirror = "{0}slackware{1}-{2}/".format(Repo().studioware(),
                                                    arch, slack_ver())

    def _init_slackr(self):
        self.mirror = Repo().slackers()

    def _init_slonly(self):
        ver = slack_ver()
        arch = "{0}-x86".format(ver)
        if os.uname()[4] == "x86_64":
            arch = "{0}-x86_64".format(ver)
        if self.meta.slack_rel == "current":
            arch = "{0}-x86_64".format(self.meta.slack_rel)
        self.mirror = "{0}{1}/".format(Repo().slackonly(), arch)

    def _init_ktown(self):
        self.mirror = Repo().ktown()

    def _init_multi(self):
        ver = slack_ver()
        if self.meta.slack_rel == "current":
            ver = self.meta.slack_rel
        self.mirror = Repo().multi() + ver + "/"

    def _init_slacke(self):
        arch = ""
        if os.uname()[4] == "x86_64":
            arch = "64"
        elif os.uname()[4] == "arm":
            arch = "arm"
        self.mirror = "{0}slacke{1}/slackware{2}-{3}/".format(
            Repo().slacke(), self.meta.slacke_sub_repo[1:-1], arch, slack_ver())

    def _init_salix(self):
        arch = "i486"
        if os.uname()[4] == "x86_64":
            arch = "x86_64"
        self.mirror = "{0}{1}/{2}/".format(Repo().salix(), arch, slack_ver())

    def _init_slackl(self):
        arch = "i486"
        if os.uname()[4] == "x86_64":
            arch = "x86_64"
        self.mirror = "{0}{1}/current/".format(Repo().slackel(), arch)

    def _init_rested(self):
        self.mirror = Repo().restricted()

    def _init_msb(self):
        arch = "x86"
        if os.uname()[4] == "x86_64":
            arch = "x86_64"
        self.mirror = "{0}{1}/{2}/{3}/".format(
            Repo().msb(), slack_ver(), self.meta.msb_sub_repo[1:-1], arch)
