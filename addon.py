# -*- coding: utf-8 -*-

'''
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
'''
from __future__ import absolute_import

from sys import argv
from tulip.compat import parse_qsl
from resources.lib import euronews

params = dict(parse_qsl(argv[2].replace('?','')))
action = params.get('action')
url = params.get('url')

if action is None:
    euronews.indexer().root()

elif action == 'programs':
    euronews.indexer().programs()

elif action == 'videos':
    euronews.indexer().videos(url)

elif action == 'live':
    euronews.indexer().live()

elif action == 'play':
    euronews.indexer().play(url)

elif action == 'clear_cache':
    from tulip.cache import clear
    clear(withyes=False)

elif action == 'settings':
    from tulip.control import openSettings
    openSettings()
