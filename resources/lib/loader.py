# -*- coding: utf-8 -*-

'''
    Euronews Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from tulip import control
from tulip import m3u8
from tulip.compat import urljoin


def stream_picker(qualities, urls):

    choice = control.selectDialog(heading=control.name(), list=qualities)

    if choice <= len(qualities) and not choice == -1:

        popped = urls[choice]

        return popped


def m3u8_picker(url):

    m3u8_playlists = m3u8.load(url).playlists

    if not m3u8_playlists:
        return url

    qualities = []
    urls = []

    for playlist in m3u8_playlists:

        quality = repr(playlist.stream_info.resolution).strip('()').replace(', ', 'x')

        if quality == 'None':
            quality = 'Auto'
        uri = playlist.uri

        if not uri.startswith('http'):

            uri = urljoin(playlist.base_uri, uri)

        qualities.append(quality)

        urls.append(uri)

    return stream_picker(qualities, urls)
