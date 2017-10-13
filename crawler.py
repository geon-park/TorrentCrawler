import urllib.request
from lxml import html
import re


class TorrentCrawler:
    def __init__(self, base_url):
        self.BASE_URL = base_url

    def make_url(self, sub_path, **parameters):
        url = self.BASE_URL + sub_path
        for k, v in parameters.items():
            url += k + '=' + urllib.request.quote(v) + '&'

        url = url.rstrip('&')
        print(url)
        return url

    def search_torrent(self, keyword, category='', decode='utf-8'):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/61.0.3163.100 Safari/537.36'

        url = self.make_url('/bbs/s.php?', **{'k': keyword, 'b': category})
        req = urllib.request.Request(url, headers={'User-Agent': user_agent})
        content = urllib.request.urlopen(req).read()
        root = html.fromstring(content)

        # to extract magnet hash key
        p = re.compile('[A-F0-9]{40}')

        # must remove tbody(//*[@id="blist"]/table/tr[3]/td[3]/a[2] -> tr[x] is loop)
        magnets = ['magnet:?xt=urn:btih:' + p.search(x).group() for x in root.xpath('//*[@id="blist"]/table/tr/td[1]/a/@href') if p.search(x)]
        titles = [x.strip() for x in root.xpath('//*[@id="blist"]/table/tr/td[3]/a[2]/text()')]
        links = root.xpath('//*[@id="blist"]/table/tr/td[3]/a[2]/@href')

        # zip magnets, titles and links
        result_list = list(zip(magnets, titles, links))
        return result_list
