# -*- coding: utf-8 -*-

'''
    Euronews Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import, unicode_literals

import json
from tulip import cache, client, control, directory, workers
from tulip.log import log_debug
from tulip.compat import urlencode, range


class indexer:

    def __init__(self):

        self.list = []
        self.base_link = 'https://www.euronews.com'
        self.api_link = 'https://api.euronews.com/ipad/'
        self.top_link = '"methodName":"content.getHome","params":{}'
        self.programs_link = '"methodName":"content.getPrograms","params":{}'
        self.program_link = '"methodName":"content.getProgramDetails","params":{"pId":"%s"}'
        self.theme_link = '"methodName":"content.getThemeDetails","params":{"tId":"%s"}'
        self.resolve_link = '"methodName":"content.getArticle","params":{"id":"%s"}'
        self.post_link = '{%s,"apiKey":"windows8Euronews-1.0","language":"%s"}'
        self.live_link = 'https://{0}.euronews.com/api/watchlive.json'
        self.img1_link = 'https://static.euronews.com/articles/programs/650x365_%s'
        self.img2_link = 'https://static.euronews.com/articles/%s/650x365_%s.jpg'
        self.lang = self.languages()

    def root(self):

        self.list = [
            {
                'title': control.lang(32001),
                'action': 'live',
                'isFolder': 'False',
                'icon': 'live.png'
            }
            ,
            {
                'title': control.lang(32002),
                'action': 'videos',
                'url': self.top_link,
                'icon': 'top.png'
            }
            ,
            {
                'title': control.lang(32003),
                'action': 'videos',
                'url': self.theme_link % '1',
                'icon': 'news.png'
            }
            ,
            {
                'title': control.lang(32004),
                'action': 'videos',
                'url': self.theme_link % '8',
                'icon': 'sports.png'
            }
            ,
            {
                'title': control.lang(32005),
                'action': 'videos',
                'url': self.theme_link % '7',
                'icon': 'business.png'
            }
            ,
            {
                'title': control.lang(32006),
                'action': 'videos',
                'url': self.theme_link % '5',
                'icon': 'europe.png'
            }
            ,
            {
                'title': control.lang(32007),
                'action': 'videos',
                'url': self.theme_link % '2',
                'icon': 'culture.png'
            }
            ,
            {
                'title': control.lang(32008),
                'action': 'videos',
                'url': self.theme_link % '3',
                'icon': 'scitech.png'
            }
            ,
            {
                'title': control.lang(32009),
                'action': 'videos',
                'url': self.theme_link % '21',
                'icon': 'travel.png'
            }
            ,
            {
                'title': control.lang(32010),
                'action': 'programs',
                'icon': 'programs.png'
            }
            ,
            {
                'title': control.lang(32221),
                'action': 'settings',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
        ]

        directory.add(self.list, content='videos')

    def programs(self):

        self.list = cache.get(self.programs_list, 24, self.programs_link, self.lang)

        if self.list is None:
            return

        for i in self.list:

            if i['title'][0].islower():

                i.update({'title': i['title'].capitalize()})

            i.update({'action': 'videos'})

        directory.add(self.list, content='videos')

    def videos(self, url):

        self.list = cache.get(self.videos_list, 1, url, self.lang)

        if self.list is None:
            return

        for i in self.list:
            i.update({'action': 'play', 'isFolder': 'False'})

        directory.add(self.list, content='videos')

    def play(self, url):

        directory.resolve(self.resolve(url, self.lang))

    def live(self):

        lang = 'www' if self.lang == 'en' else self.lang

        stream = self.resolve_live(lang=lang)

        if control.setting('quality_live') == '2' and control.kodi_version() >= 18.0:

            dash = True
            manifest_type = 'hls'
            mimetype= 'application/vnd.apple.mpegurl'

        else:

            dash = False
            manifest_type = None
            mimetype = None

        directory.resolve(
            stream, meta={'title': 'Euronews'}, dash=dash, manifest_type=manifest_type,
            mimetype=mimetype
        )

    def languages(self):

        lang_setting = control.setting('language')

        if lang_setting == '0':

            langDict = {
                'French': 'fr',
                'German': 'de',
                'Greek': 'gr',
                'Hungarian': 'hu',
                'Italian': 'it',
                'Portuguese': 'pt',
                'Russian': 'ru',
                'Spanish': 'es',
                'Turkish': 'tr',
                'Ukrainian': 'ua'  #,
                # 'Arabic': 'arabic',
                # 'Persian': 'fa'
            }

            try:
                import xbmc
                lang = langDict[xbmc.getLanguage(xbmc.ENGLISH_NAME).split(' ')[0]]
            except KeyError:
                lang = 'en'

        else:
            langDict = {
                '2': 'fr',
                '3': 'de',
                '4': 'gr',
                '5': 'hu',
                '6': 'it',
                '7': 'pt',
                '8': 'ru',
                '9': 'es',
                '10': 'tr',
                '11': 'ua'  #,
                # '12': 'arabic',
                # '13': 'fa'
            }

            try:
                lang = langDict[lang_setting]
            except KeyError:
                lang = 'en'

        return lang

    def programs_list(self, url, lang):

        try:

            request = urlencode({'request': self.post_link % (url, lang)})

            result = client.request(self.api_link, post=request)

            result = json.loads(result)

            items = result['programs']

        except:

            return

        for item in items:

            try:

                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                url = str(item['pId'])
                url = self.program_link % url
                url = url.encode('utf-8')

                image = item['img']
                image = self.img1_link % image
                image = image.encode('utf-8')

                self.list.append({'title': title, 'url': url, 'image': image})

            except:

                pass

        return self.list

    def videos_list(self, url, lang):

        try:

            request = urlencode({'request': self.post_link % (url, lang)})

            result = client.request(self.api_link, post=request)

            result = json.loads(result)

            items = []

            if 'themedetailslist' in result:
                items = result['themedetailslist']

            elif 'programDetailsList' in result:
                items = result['programDetailsList']

            elif 'homelist' in result:
                items = result['homelist']

        except:

            return

        for item in items:

            try:

                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                url = str(item['id'])
                url = url.encode('utf-8')

                image = self.img2_link % (url, url)
                image = image.encode('utf-8')

                self.list.append({'title': title, 'url': url, 'image': image})

            except:

                pass

        threads = []
        for i in list(range(0, len(self.list))):
            threads.append(workers.Thread(self.list_worker, i, lang))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if 'check' in i and not (i['check'] == '' or i['check'] is None)]

        return self.list

    def list_worker(self, i, lang):

        try:

            url = self.list[i]['url']
            check = self.resolve(url, lang)
            self.list[i].update({'check': check})

        except:

            pass

    def resolve(self, url, lang):

        url = self.resolve_link % url

        request = urlencode({'request': self.post_link % (url, lang)})

        result = client.request(self.api_link, post=request)

        url = json.loads(result)['articlelist']['videoUri']

        return url

    def resolve_live(self, lang):

        result = client.request(self.live_link.format(lang), error=True)
        result = json.loads(result)['url']

        if result.startswith('//'):
            result = 'http:' + result

        result = client.request(result, error=True)

        _json = json.loads(result)

        try:
            if _json.get('status') == 'ko':
                control.infoDialog(_json.get('msg').capitalize(), time=5000)
                log_debug(_json.get('msg').capitalize())
                return
        except Exception:
            return

        if control.setting('backup_live') == 'false':
            stream = _json['primary']
        else:
            stream = _json['backup']

        if stream.startswith('//'):

            stream = ''.join(['http:', stream])

        if control.setting('quality_live') in ['0', '2']:
            return stream
        else:
            from resources.lib.loader import m3u8_picker
            return m3u8_picker(stream)
