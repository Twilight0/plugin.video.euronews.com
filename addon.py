# -*- coding: utf-8 -*-

'''
    Euronews Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
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
