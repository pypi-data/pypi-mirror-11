#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Alex Turbov <i.zaufi@gmail.com>
#
# JIRA Bot is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# JIRA Bot is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys

from jira_bot.fancy_grid import FancyGrid

class ListPrioritiesSubCommand:
    def __init__(self, subparsers):
        parser = subparsers.add_parser(
            'list-priorities'
          , help='Show list of configured priorities'
          )

        parser.set_defaults(func=self._list_priorities)


    def _list_priorities(self, conn, config):
        priorities = [(p.id, p.name) for p in conn.priorities()]
        print(FancyGrid(priorities))
